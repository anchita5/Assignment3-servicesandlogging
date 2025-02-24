/*
FILE          : client test.cpp
PROJECT       : Assignment 2 - NAD
PROGRAMMER    : Anchita Kakria, Uttam Arora
FIRST VERSION : 23 Feb 2025
DESCRIPTION   : This cpp file implemets a simple tcp that will send messages to the server.
                It will do both manual and automatic log entry.
*/


#include <iostream>
#include <string>
#include <vector>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "Ws2_32.lib")
//comment to check
//uttam commented

using namespace std;

/*
 * FUNCTION    : sendLogMessage
 * DESCRIPTION : This function sends a log message to the server using TCP and also recieve the server's response
 * PARAMETERS  : const string& serverIP: Ip os server
 *               int port: port number
 *               const string& message: log message that will be sent
 * RETURNS     : none
 */

void sendLogMessage(const string& serverIP, int port, const string& message) {
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData); //initializing

    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0); //creating a socket here. it will communicate
    if (sock == INVALID_SOCKET) { //checking
        cerr << "Socket creation failed." << endl; //error message if it fails
        return;
    }

    sockaddr_in serverAddr; //server address will be held
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    inet_pton(AF_INET, serverIP.c_str(), &serverAddr.sin_addr);

    if (connect(sock, (sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) { //connection to server with IP and port
        cerr << "Connection to server failed." << endl; //error message if it fails
        closesocket(sock); //closes after sending the message
        WSACleanup();
        return;
    }

    send(sock, message.c_str(), message.size(), 0); //sending the message to sevrer

    char buffer[1024] = { 0 }; //buffer to store the response
    recv(sock, buffer, sizeof(buffer), 0); //recieved message will be stored here in the buffer
    cout << "Server Response: " << buffer << endl; //message recieved by server

    closesocket(sock);
    WSACleanup();
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cout << "Usage: client <server_ip> <port>" << endl; //printing the usage info
        return 1;  //return with error if something is missing
    }

    string serverIP = argv[1]; // server's IP
    int port = stoi(argv[2]); //port

    int choice;
    cout << "Select mode:\n1. Manual Log Entry\n2. Automatic Log Testing\nEnter choice: ";
    cin >> choice;
    cin.ignore(); // clear the input buffer

    if (choice == 1) {
        // maually entering log
        string message;
        cout << "Enter log message: ";
        getline(cin, message);
        sendLogMessage(serverIP, port, message);
    }
    else if (choice == 2) {
        // automatic log test
        vector<string> testMessages = {
            "INFO: User logged in",
            "WARNING: High memory usage detected",
            "ERROR: Failed to connect to database",
            "DEBUG: Variable x = 10",
            "CRITICAL: System shutdown imminent"
        };

        for (const string& message : testMessages) {
            sendLogMessage(serverIP, port, message);
            Sleep(1000);  // wait 1 second to avoid rate limiting
        }
    }
    else {
        cout << "Invalid choice. Exiting." << endl; //message
    }

    return 0;
}
