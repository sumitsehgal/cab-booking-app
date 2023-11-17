//
//  Navigation.swift
//  Cuber
//
//  Created by Virus Macbook on 14/11/23.
//

import SwiftUI
import MapKit

struct MapNavigationTest: View {
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    )

    @State private var destinationCoordinate = CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.431297)

    var body: some View {
        NavigationView {
            VStack {
                Map(coordinateRegion: $region), annotationItems: [destinationCoordinate]) { coordinate in
                    MapPin(coordinate: coordinate, tint: .red)
                }
                .onAppear {
                    calculateDirection()
                }

                Spacer()

                Text("Navigate to Destination")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                    .onTapGesture {
                        navigateToDestination()
                    }
            }
            .navigationTitle("Map Navigation")
        }
    }

    private func calculateDirection() {
        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: region.center))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destinationCoordinate))
        request.transportType = .automobile

        let directions = MKDirections(request: request)
        directions.calculate { response, error in
            guard let route = response?.routes.first else {
                if let error = error {
                    print("Error calculating directions: \(error.localizedDescription)")
                }
                return
            }

            region = MKCoordinateRegion(route.polyline.boundingMapRect)
        }
    }

    private func navigateToDestination() {
        let mapItem = MKMapItem(placemark: MKPlacemark(coordinate: destinationCoordinate))
        mapItem.name = "Destination"
        mapItem.openInMaps(launchOptions: [MKLaunchOptionsDirectionsModeKey: MKLaunchOptionsDirectionsModeDriving])
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        MapNavigationTest()
    }
}
