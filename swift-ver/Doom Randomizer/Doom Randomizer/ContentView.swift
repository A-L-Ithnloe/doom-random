//
//  ContentView.swift
//  Doom Randomizer
//
//  Created by Quantori on 09.01.24.
//

import SwiftUI

extension UIScreen {
   static let screenWidth = UIScreen.main.bounds.size.width
   static let screenHeight = UIScreen.main.bounds.size.height
   static let screenSize = UIScreen.main.bounds.size
}

struct MainFrame: View {
    @State private var path = NavigationPath()
    
    var body: some View {
        VStack {
            Text("Welcome to Doom Randomizer")
            .font(.custom("CourierNewPS-BoldMT", size: UIScreen.screenWidth.truncatingRemainder(dividingBy: 37.0)))
            .fontWeight(.bold)
            
        }
        NavigationStack {
            HStack {
                VStack(alignment: .leading) {
                    Button("WADs") {
                        path.append("WADs")
                    }
                    .font(.system(size: 25))
                    .buttonStyle(.borderedProminent)
                    .fontWeight(.regular)
                    .offset(y: 50)
                    .padding()
                    .navigationDestination(for: String.self) { route in switch
                        route {
                            case "WADs":
                                WADs()
                            default:
                                MainFrame()
                        }
                    }
                    
                    Button("Loadouts") {
                        path.append("Loadouts")
                    }
                    .font(.system(size: 25))
                    .buttonStyle(.borderedProminent)
                    .fontWeight(.regular)
                    .offset(y: 30)
                    .padding()
                    .navigationDestination(for: String.self) { route in switch
                        route {
                            case "Loadouts":
                        Loadouts()
                            default:
                                MainFrame()
                        }
                    }
                    
                    Button("RANDOMIZE") {
                        // Generate WAD + Playstyle + Loadout
                    }
                    .font(.system(size: 35))
                    .buttonStyle(.borderedProminent)
                    .tint(.purple)
                    .fontWeight(.medium)
                    .padding()
                }
                //.fixedSize(horizontal: false, vertical: true)
                
                VStack (alignment: .trailing) {
                    Button("Playstyles") {
                        path.append("Playstyles")
                    }
                    .font(.system(size: 25))
                    .buttonStyle(.borderedProminent)
                    .fontWeight(.regular)
                    .offset(y: 50)
                    .padding()
                    .navigationDestination(for: String.self) { route in switch
                        route {
                            case "Playstyles":
                                Playstyles()
                            default:
                                MainFrame()
                        }
                    }
                        
                    Button("Downloads") {
                        path.append("Downloads")
                    }
                    .font(.system(size: 25))
                    .buttonStyle(.borderedProminent)
                    .fontWeight(.regular)
                    .offset(y: 30)
                    .padding()
                    .navigationDestination(for: String.self) { route in switch
                        route {
                            case "Downloads":
                                Downloads()
                            default:
                                MainFrame()
                        }
                    }
                        
                    Button("PICK DOWNLOAD") {
                        // Pick from Download List
                    }
                    .font(.system(size: 35))
                    .buttonStyle(.borderedProminent)
                    .tint(.purple)
                    .fontWeight(.medium)
                    .padding()
                }
                //.fixedSize(horizontal: false, vertical: true)
            }
        }
        Spacer()
        
        TextField("Results", text: /*@START_MENU_TOKEN@*//*@PLACEHOLDER=Value@*/.constant("")/*@END_MENU_TOKEN@*/)
            .multilineTextAlignment(.center)
            .frame(width: 450, height: 400)
            .border(.black)
            .fontWeight(.regular)
    }
}

struct WADs: View {
    @Environment(\.dismiss) private var dismiss
    //@Binding var path = NavigationPath
    
    var body: some View {
        Button("Back") {
            dismiss()
        }
        .font(.system(size: 25))
        .buttonStyle(.borderedProminent)
        .fontWeight(.regular)
    }
}

struct Playstyles: View {
    @Environment(\.dismiss) private var dismiss
    //@Binding var path = NavigationPath
    
    var body: some View {
        Button("Back") {
            dismiss()
        }
        .font(.system(size: 25))
        .buttonStyle(.borderedProminent)
        .fontWeight(.regular)
    }
}

struct Loadouts: View {
    @Environment(\.dismiss) private var dismiss
    //@Binding var path = NavigationPath
    
    var body: some View {
        Button("Back") {
            dismiss()
        }
        .font(.system(size: 25))
        .buttonStyle(.borderedProminent)
        .fontWeight(.regular)
    }
}

struct Downloads: View {
    @Environment(\.dismiss) private var dismiss
    //@Binding var path = NavigationPath
    
    var body: some View {
        Button("Back") {
            dismiss()
        }
        .font(.system(size: 25))
        .buttonStyle(.borderedProminent)
        .fontWeight(.regular)
    }
}

#Preview {
    MainFrame()
}
