import SwiftUI
import MapKit

struct MapViewTest: View {
    @State private var region = MKCoordinateRegion(
        center: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194),
        span: MKCoordinateSpan(latitudeDelta: 0.05, longitudeDelta: 0.05)
    )

    var body: some View {
        Map(coordinateRegion: $region, showsUserLocation: true, userTrackingMode: .constant(.follow), annotationItems: locations) { location in
            MapPin(coordinate: location.coordinate, tint: .blue)
        }
        .onAppear {
            // Load your locations data or update the region as needed
            // For example, you could fetch locations from a database or API
        }
    }

    let locations: [MapLocation] = [
        MapLocation(title: "San Francisco", subtitle: "California", coordinate: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194)),
        MapLocation(title: "New York", subtitle: "New York", coordinate: CLLocationCoordinate2D(latitude: 40.7128, longitude: -74.0060)),
        // Add more locations as needed
    ]
}

struct MapLocation: Identifiable {
    let id = UUID()
    let title: String?
    let subtitle: String?
    let coordinate: CLLocationCoordinate2D
}

#Preview {
    MapViewTest()
}
