#include <iostream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "Ws2_32.lib")
//comment to check
//uttam commented

using namespace std;

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