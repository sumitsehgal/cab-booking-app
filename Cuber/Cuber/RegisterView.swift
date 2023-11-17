//
//  UserDetailView.swift
//  Cuber
//
//  Created by Virus Macbook on 12/11/23.
//

import SwiftUI

struct RegisterView: View {
    @State private var username = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    @State private var firstName = ""
    @State private var middleName = ""
    @State private var lastName = ""
    @State private var city = ""
    @State private var phoneNumber = ""
    @State private var emergencyContacts = ""

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Account Information")) {
                    TextField("Username", text: $username)
                        .autocapitalization(.none)
                    SecureField("Password", text: $password)
                    SecureField("Confirm Password", text: $confirmPassword)
                }

                Section(header: Text("Personal Information")) {
                    TextField("First Name", text: $firstName)
                    TextField("Middle Name", text: $middleName)
                    TextField("Last Name", text: $lastName)
                    TextField("Ciity", text: $city)
                    TextField("Phone Number", text: $phoneNumber)
                        .keyboardType(.phonePad)
                    TextField("Emergency Contacts", text: $emergencyContacts)
                }

                Section {
                    HStack {
                        Button(action: {
                            // Perform registration logic here
                            self.register()
                        }) {
                            Text("Register")
                                .frame(maxWidth: .infinity)
                                .padding()
                                .foregroundColor(.white)
                                .background(Color.blue)
                                .cornerRadius(8)
                        }
                        .buttonStyle(DefaultButtonStyle())

                        Button(action: {
                            // Perform user details update logic here
                            self.updateUserDetails()
                        }) {
                            Text("Save Changes")
                                .frame(maxWidth: .infinity)
                                .padding()
                                .foregroundColor(.white)
                                .background(Color.green)
                                .cornerRadius(8)
                        }
                        .buttonStyle(DefaultButtonStyle())
                    }
                }
            }
            .navigationBarTitle("Personal Details")
        }
    }

    func register() {
        // Your registration logic here
    }

    func updateUserDetails() {
        // Your update logic here
    }
}

struct CombinedForm_Previews: PreviewProvider {
    static var previews: some View {
        RegisterView()
    }
}
