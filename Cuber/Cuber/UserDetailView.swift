//
//  UserDetailView.swift
//  Cuber
//
//  Created by Virus Macbook on 12/11/23.
//

import SwiftUI

struct UserDetailView: View {
    @State private var firstName = ""
    @State private var middleName = ""
    @State private var lastName = ""
    @State private var city = ""
    @State private var phoneNumber = ""
    @State private var emergencyContacts = ""
    @State private var requestUrl = "http://localhost:8080/api/v1/user"
    @State private var showAlert: Bool = false
    @State private var message: String = ""
    @State private var alertTitle: String = ""
    @State private var email: String = ""
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Personal Information")) {
                    TextField("First Name", text: $firstName)
                    TextField("Middle Name", text: $middleName)
                    TextField("Last Name", text: $lastName)
                    TextField("Email", text: $email)
                    TextField("City", text: $city)
                    TextField("Phone Number", text: $phoneNumber)
                        .keyboardType(.phonePad)
                    TextField("Emergency Contacts", text: $emergencyContacts)
                }

                Section {
                    Button(action: {
                        // Perform user details update logic here
                        self.registerUser()
                    }) {
                        Text("Register")
                            .frame(maxWidth: .infinity)
                            .padding()
                            .foregroundColor(.white)
                            .background(Color.blue)
                            .cornerRadius(8)
                    }
                    .buttonStyle(DefaultButtonStyle())
                }
            }
            .navigationBarTitle("User Details")
            .alert(isPresented: $showAlert){
                Alert( title: Text(alertTitle), message: Text(message), dismissButton: .default(Text("Ok")))
            }
        }
    }

    func registerUser() {
        // Validate inputs
        guard !firstName.isEmpty, !phoneNumber.isEmpty, !email.isEmpty else {
            print("First Name, Mobile Number and Email is mandatory")
            showAlert = true
            alertTitle = "Error"
            message = "First Name, Mobile Number and Email fields are Mandatory"
            return
        }

        // Construct the update user details URL
        let updateUserDetailsURL = URL(string: requestUrl)!

        // Create update user details parameters
        let parameters: [String: String] = [
            "first_name": firstName,
            "middle_name": middleName,
            "last_name": lastName,
            "email": email,
            "city": city,
            "mobile_number": phoneNumber,
            "emergency_contact" : emergencyContacts
        ]

        // Create the HTTP request
        var request = URLRequest(url: updateUserDetailsURL)
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
                print("Update user details failed with error: \(error)")
                alertTitle = "Error"
                message = "Failed to register user"
                showAlert = true
                return
            }

            if let data = data {
                // Parse the response data if needed
                // For now, just print the response as a string
                if let responseString = String(data: data, encoding: .utf8) {
                    do {
                        let decoder = JSONDecoder()
                        // Assuming that Post is a Codable struct or class
                        let decodedData = try decoder.decode(RequestResponse.self, from: data)
                        DispatchQueue.main.async {
                            if decodedData.status == "Error"{
                                alertTitle = "Error"
                                message = "Failed to register user"
                                showAlert = true
                            }
                            else{
                                message = "User registered"
                                alertTitle = "Success"
                                showAlert = true
                            }
                        }
                    } catch {
                        print("Error decoding JSON: \(error)")
                    }
                }
            }
        }.resume()
    }
}

struct RequestResponse: Codable{
    let status: String
    let message: String
    
    private enum CodingKeys: String, CodingKey {
        case status = "status"
        case message = "message"
    }
    
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        status = try container.decode(String.self, forKey: .status)
        message = try container.decode(String.self, forKey: .message)
    }
}

struct UserDetailsForm_Previews: PreviewProvider {
    static var previews: some View {
        UserDetailView()
    }
}
