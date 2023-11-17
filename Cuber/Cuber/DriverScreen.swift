//
//  DriverScreen.swift
//  Cuber
//
//  Created by Virus Macbook on 17/11/23.
//

import SwiftUI

struct DriverBookingData: Identifiable, Codable {
    let bookingId: String
    let dropLocation: [Double]
    let pickUpLocation: [Double]
    
    var id: String {
        return bookingId
    }
    
    private enum CodingKeys: String, CodingKey {
        case bookingId = "booking_id"
        case dropLocation = "drop_location"
        case pickUpLocation = "user_location"
    }
}


struct DriverActionResponse: Identifiable, Codable{
    
    let bookingId: String
    let status: String
    let userLocation: [Double]
    let destination: [Double]
    
    var id: String{
        return bookingId
    }
    
    private enum CodingKeys: String,CodingKey{
        case bookingId = "booking_id"
        case status = "status"
        case destination = "destination"
        case userLocation = "user_location"
    }
}

struct DriverScreenTripView: View {
    @State private var bookings: [DriverBookingData] = []
    @State private var timer: Timer?
    @State private var showAlert: Bool = false
    @State private var alertTitle: String = ""
    @State private var message: String = ""
    
    // Ideally this will be set by profile
    @State private var taxiId: String = "Taxi-11"
    @State private var baseUrl: String = "http://localhost:8090/api/v1/"

    

    var body: some View {
        NavigationView {
            List(bookings) { booking in
                VStack(alignment: .leading) {
                    Text("Booking ID: \(booking.bookingId)")
                    Text("Drop Location: \(booking.dropLocation[0]), \(booking.dropLocation[1])")
                    Text("Pickup Location: \(booking.pickUpLocation[0]), \(booking.pickUpLocation[1])")
                }
                .padding()

                HStack {
                    Button(action: {sendDriverRequest(bookingId: booking.bookingId, driverAction: "Accept")}, label: {
                        Text("Accept")
                    }).foregroundColor(.green)
                    
                    Spacer()
                    
                    Button(action: {sendDriverRequest(bookingId: booking.bookingId, driverAction: "Reject")}, label: {
                        Text("Reject")
                    }).foregroundColor(.red)
                    
                }
                .padding(.horizontal)
            }
            .navigationTitle("Driver Bookings")
            .onAppear {
                fetchData() // Initial data fetch
                startTimer() // Start the timer for polling
            }
            .onDisappear {
                stopTimer() // Stop the timer when the view disappears
            }.alert(isPresented: $showAlert){
                Alert( title: Text(alertTitle), message: Text(message), dismissButton: .default(Text("Ok")))
            }
        }
    }
    
    func sendDriverRequest(bookingId: String, driverAction: String){
        guard let driverActionURL = URL(string: baseUrl + "booking/driver/action") else {
            print("Invalid URL")
            return
        }

        let parameters: [String : Any] = [
            "taxi_id" : taxiId,
            "booking_id" : bookingId,
            "status" : driverAction
        ]
        
        var request = URLRequest(url: driverActionURL)
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
                    let decodedData = try decoder.decode(DriverActionResponse.self, from: data)
                    DispatchQueue.main.async {
                        message = "Booking " + decodedData.bookingId
                        alertTitle = decodedData.status
                        showAlert = true
                    }
                } catch {
                    print("Error decoding JSON: \(error)")
                }
            }
        }.resume()
        
        
    }

    private func fetchData() {
        guard let checkBookingURL = URL(string: baseUrl + "/booking/check/trip") else {
            print("Invalid URL")
            return
        }

        let parameters: [String : Any] = [
            "taxi_id" : taxiId,
        ]
        
        var request = URLRequest(url: checkBookingURL)
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
                    let decodedData = try decoder.decode([DriverBookingData].self, from: data)
                    DispatchQueue.main.async {
                        print(decodedData)
                        bookings = decodedData
                    }
                } catch {
                    print("Error decoding JSON: \(error)")
                }
            }
        }.resume()
    }

    private func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { _ in
            fetchData() // Fetch data every 10 seconds
        }
    }

    private func stopTimer() {
        timer?.invalidate()
    }
}


#Preview {
    DriverScreenTripView()
}

