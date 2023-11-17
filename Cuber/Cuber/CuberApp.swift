//
//  CuberApp.swift
//  Cuber
//
//  Created by Virus Macbook on 11/11/23.
//

import SwiftUI

@main
struct CuberApp: App {
    @AppStorage("showMenuBarExtra") private var showMenuBarExtra = true
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
