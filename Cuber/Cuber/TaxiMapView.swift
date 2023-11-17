//
//  TaxiMapView.swift
//  Cuber
//
//  Created by Virus Macbook on 12/11/23.
//

import SwiftUI
import MapKit

struct TaxiMapView: View {
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    )

    // Sample taxi locations
    let taxiLocations: [TaxiLocation] = [
        TaxiLocation(name: "Taxi 1", coordinate: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194)),
        TaxiLocation(name: "Taxi 2", coordinate: CLLocationCoordinate2D(latitude: 37.7750, longitude: -122.4195)),
        // Add more taxi locations as needed
    ]

    var body: some View {
        Map(coordinateRegion: $region, showsUserLocation: true, annotationItems: taxiLocations) { taxi in
            MapPin(coordinate: taxi.coordinate, tint: .blue)
        }
        .navigationBarTitle("Taxi Map")
    }
}

struct TaxiLocation: Identifiable {
    let id = UUID()
    let name: String
    let coordinate: CLLocationCoordinate2D
}

struct TaxiMapView_Previews: PreviewProvider {
    static var previews: some View {
        TaxiMapView()
    }
}


#Preview {
    TaxiMapView()
}
