//
//  ContentView.swift
//  Cuber
//
//  Created by Virus Macbook on 11/11/23.
//

import SwiftUI
import MapKit

struct ContentView: View {
    @State private var text: String = ""
    var body: some View {
        /*VStack {
         SearchCabView().frame(height: 500)
         }
         .padding()
         */
        
        /*
        NavigationView {
            NavigationLink(destination: SecondView(text: $text)) {
                Text("Navigate to Second Screen")
            }.navigationBarTitle("First Screen")
        }
        Text(text)
        */
        TabView{
            SearchCabView().tabItem {
                Image(systemName: "house")
                Text("Home")
            }
            UserDetailView().tabItem {
                Image(systemName: "gear")
                Text("Setting")
            }
            DriverScreenTripView().tabItem {
                Image(systemName: "car")
                Text("Driver Trip")
            }
        }
        
    }
}

struct StatusMenu: View {
    func action1() {}
    func action2() {}
    func action3() {}

    var body: some View {
        Button(action: action1, label: { Text("Action 1") })
        Button(action: action2, label: { Text("Action 2") })
        
        Divider()

        Button(action: action3, label: { Text("Action 3") })
    }
}

struct SecondView: View {
    @Binding var text: String

    var body: some View {
        TextField("Enter text", text: $text)
            .navigationBarTitle("Second Screen")
    }
}

#Preview {
    ContentView()
}
