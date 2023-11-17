//
//  MapView.swift
//  Cuber
//
//  Created by Virus Macbook on 11/11/23.
//
import SwiftUI
import MapKit

struct MapView: View {
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    )

    let locations: [Location] = [
        Location(name: "Marker 1", latitude: 37.7750, longitude: -122.4195),
        Location(name: "Marker 2", latitude: 37.7760, longitude: -122.4185),
        Location(name: "Marker 3", latitude: 37.7745, longitude: -122.4205)
    ]

    var body: some View {
        Map(coordinateRegion: $region, showsUserLocation: true, annotationItems: locations) { location in
            MapAnnotation(coordinate: CLLocationCoordinate2D(latitude: location.latitude, longitude: location.longitude)) {
                Image(systemName: "car")
                    .resizable()
                    .frame(width: 30, height: 30)
                    .foregroundColor(.blue)
            }
        }
        .onAppear {
            // Optionally, you can adjust the region to fit all markers when the view appears
            region = regionThatFitsAllLocations()
        }
        .navigationBarTitle("Map with Markers")
    }

    func regionThatFitsAllLocations() -> MKCoordinateRegion {
        var minLat = locations.first?.latitude ?? 0
        var maxLat = locations.first?.latitude ?? 0
        var minLon = locations.first?.longitude ?? 0
        var maxLon = locations.first?.longitude ?? 0

        for location in locations {
            minLat = min(minLat, location.latitude)
            maxLat = max(maxLat, location.latitude)
            minLon = min(minLon, location.longitude)
            maxLon = max(maxLon, location.longitude)
        }

        let center = CLLocationCoordinate2D(latitude: (minLat + maxLat) / 2, longitude: (minLon + maxLon) / 2)
        let span = MKCoordinateSpan(latitudeDelta: maxLat - minLat, longitudeDelta: maxLon - minLon)

        return MKCoordinateRegion(center: center, span: span)
    }
}

struct Location: Identifiable {
    let id = UUID()
    let name: String
    let latitude: Double
    let longitude: Double
}

struct MapView_Previews: PreviewProvider {
    static var previews: some View {
        MapView()
    }
}
