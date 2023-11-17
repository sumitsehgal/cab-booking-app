//
//  SearchCabView.swift
//  Cuber
//
//  Created by Virus Macbook on 11/11/23.
//

import SwiftUI
import MapKit

struct SearchCabView: View {
    @State private var pickUpLocation: String = "Test Location"
    @State private var destinationLocation: String = "Test Destination"
    @State private var requestBaseUrl: String = "http://localhost:8090/api/v1/"
    @State private var userId: String = "First Name-65478"
    @State private var taxiLocations: [TaxiLocation] = []
    @State private var bookingId: String = ""
    
    @State private var showAlert: Bool = false
    @State private var alertTitle: String = ""
    @State private var message: String = ""
    @State private var booking: String = ""
    @State private var taxiId: String = ""
    @State private var taxiLocation: [Double] = []
    
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 21.169676702877396, longitude: 78.97251758689261),
        span: MKCoordinateSpan(latitudeDelta:0.1, longitudeDelta:0.1)
    )
    
    
    @State var userLocation = CLLocationCoordinate2D(latitude: 21.169676702877396, longitude: 78.97251758689261)
    
    
    
    func bookCabs() {
        guard !pickUpLocation.isEmpty, !destinationLocation.isEmpty else {
            print("Pick up location and destination cannot be empty")
            message = "Cannot be empty"
            alertTitle = "Error"
            showAlert = true
                return
        }
        
        let bookCabs = URL(string: requestBaseUrl + "booking/confirm")!
        //let geocoder = CLGeocoder()
        
        let parameters: [String : Any] = [
            "user_id" : userId,
            "user_location" : [21.169676702877396,78.97251758689261],
            "destination": [13.160277872294213,80.18578008595382]
        ]
        
        var request = URLRequest(url: bookCabs)
        request.httpMethod = "POST"
        request.timeoutInterval = 200 // setting timeout to 200 secoonds
        do{
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters)
        }catch{
            print("Error in encoding requested data")
            return
        }
        
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            // Handle the response here
            if let error = error {
                print("No cabs found: \(error)")
                return
            }

            if let data = data {
                do {
                    let decoder = JSONDecoder()
                    // Assuming that Post is a Codable struct or class
                    let decodedData = try decoder.decode(ConfirmBookingData.self, from: data)
                    DispatchQueue.main.async {
                        print(decodedData.status)
                        if decodedData.status != "No-Cabs"{
                            booking = decodedData.bookingId
                            taxiId = decodedData.taxiAlloted
                            taxiLocation = decodedData.cabLocation
                            message = "Taxi Alloted " + taxiId
                            alertTitle = "Success"
                            showAlert = true
                        }
                        else{
                            message = "Sorry, couldn't find cab for you"
                            alertTitle = "Failed"
                            showAlert = true
                        }
                    }
                } catch {
                    print("Error decoding JSON: \(error)")
                }
            }
        }.resume()
    }
    
    func findCabs() {
        // Validate inputs
        guard !pickUpLocation.isEmpty, !destinationLocation.isEmpty else {
            print("First Name and Mobile Number is mandatory")
            return
        }

        // Construct the update user details URL
        let findCabs = URL(string: requestBaseUrl + "booking/cabs")!

        // Create update user details parameters
        let parameters: [String: Any] = [
            "user_id": userId,
            "user_location" : [21.169676702877396,78.97251758689261],
            "destination" : [13.160277872294213,80.18578008595382]
        ]

        // Create the HTTP request
        var request = URLRequest(url: findCabs)
        request.httpMethod = "POST"

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: parameters)
        } catch {
            print("Error encoding update user details parameters: \(error)")
            return
        }

        // Set the content type
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        // Make the HTTP request
        URLSession.shared.dataTask(with: request) { data, response, error in
            // Handle the response here
            if let error = error {
                print("No cabs found: \(error)")
                return
            }

            if let data = data {
                do {
                    let decoder = JSONDecoder()
                    // Assuming that Post is a Codable struct or class
                    let decodedData = try decoder.decode(BookingDetails.self, from: data)
                    DispatchQueue.main.async {
                        self.taxiLocations = decodedData.getTaxis()
                        print(self.taxiLocations)
                    }
                } catch {
                    print("Error decoding JSON: \(error)")
                }
            }
        }.resume()
    }
    
    
    func regionThatFitsAllLocations() -> MKCoordinateRegion {
        var minLat = self.taxiLocations.first?.latitude ?? 0
        var maxLat = self.taxiLocations.first?.latitude ?? 0
        var minLon = self.taxiLocations.first?.longitude ?? 0
        var maxLon = self.taxiLocations.first?.longitude ?? 0
        
        for location in self.taxiLocations {
            minLat = min(minLat, location.latitude)
            maxLat = max(maxLat, location.latitude)
            minLon = min(minLon, location.longitude)
            maxLon = max(maxLon, location.longitude)
        }
        
        let center = CLLocationCoordinate2D(latitude: (minLat + maxLat) / 2, longitude: (minLon + maxLon) / 2)
        let span = MKCoordinateSpan(latitudeDelta: maxLat - minLat, longitudeDelta: maxLon - minLon)
        
        return MKCoordinateRegion(center: center, span: span)
    }
    
    var body: some View {
        VStack{
            let locationManager = CLLocationManager()
            Form{
                TextField(
                    "Pick Up Location",
                    text: $pickUpLocation
                )
                
                TextField(
                    "Destination",
                    text: $destinationLocation
                )
                
                
                Button(action: {
                    // Perform user details update logic here
                    self.bookCabs()
                }) {
                    Text("Book")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .foregroundColor(.white)
                        .background(Color.blue)
                        .cornerRadius(8)
                }
                .buttonStyle(DefaultButtonStyle())
                
            }.frame(height: 200)
            
            //Map(initialPosition: .region(region)).frame(height: 500)
            Map(coordinateRegion: $region, showsUserLocation: true,userTrackingMode:.constant(.follow), annotationItems: self.taxiLocations){
                taxi in MapAnnotation(coordinate: CLLocationCoordinate2D(latitude: taxi.latitude, longitude: taxi.longitude)){
                    VStack{
                        Image(systemName: "car")
                            .resizable()
                            .frame(width: 30, height: 40)
                            .foregroundColor(.black)
                        Text(String(taxi.distance) + " mins")
                    }
                }
            }.onAppear{
                locationManager.requestWhenInUseAuthorization()
                findCabs()
            }.alert(isPresented: $showAlert){
                Alert( title: Text(alertTitle), message: Text(message), dismissButton: .default(Text("Ok")))
            }
            
        }
    }
}



struct ConfirmBookingData: Identifiable, Codable{
    let bookingId: String
    let status: String
    let taxiAlloted: String
    let userLocation: [Double]
    let cabLocation: [Double]
    
    private enum CodingKeys: String, CodingKey{
        case bookingId = "booking_id"
        case status = "status"
        case taxiAlloted = "taxi_alloted"
        case userLocation = "user_location"
        case cabLocation = "cab_location"
    }
    
    var id: String {
        return bookingId
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        bookingId = try container.decode(String.self, forKey: .bookingId)
        print(bookingId)
        status = try container.decode(String.self, forKey: .status)
        print(status)
        taxiAlloted = try container.decode(String.self, forKey: .taxiAlloted)
        print(taxiAlloted)
        userLocation = try container.decode([Double].self, forKey: .userLocation)
        print(userLocation)
        cabLocation = try container.decode([Double].self, forKey: .cabLocation)
        print(cabLocation)
    }
}

struct TaxiLocation: Identifiable {
    let id = UUID()
    let name: String
    let latitude: Double
    let longitude: Double
    let distance: Int
}


struct BookingDetails: Identifiable, Codable {
    let taxisLocation: [[Double]]
    let userId: String

    
    private enum CodingKeys: String, CodingKey {
        case taxisLocation = "taxis_location"
        case userId = "user_id"
    }
    
    var id: String {
        return userId
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        taxisLocation = try container.decode([[Double]].self, forKey: .taxisLocation)
        userId = try container.decode(String.self, forKey: .userId)
    }
    
    func getTaxis() ->[TaxiLocation]{
        var tempTaxis: [TaxiLocation] = []
        
        for l in taxisLocation{
            tempTaxis.append(TaxiLocation(name:"Taxi", latitude: l[0], longitude: l[1], distance: Int(l[2])))
        }
        return tempTaxis
    }
}


#Preview {
    SearchCabView()
}
