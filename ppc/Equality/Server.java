import java.lang.management.ThreadInfo;
import java.net.ServerSocket;
import java.net.Socket;

class Server
{
    private ServerSocket serverSocket;
    private int portNumber;
    Server(int portNumber)
    {
        this.portNumber=portNumber;
        try
        {//Initiating ServerSocket with TCP port
            serverSocket=new ServerSocket(this.portNumber);
            startListening();
        }catch(Exception e)
        {
            System.out.println(e);
            System.exit(0);
        }
    }
private void startListening()
{
    try
    {
        Socket socket;
        while(true)
        {
            System.out.println("Server is listening on port : "+this.portNumber);
            socket=serverSocket.accept(); // server is in listening mode
            System.out.println("Request arrived..");// diverting the request to processor with the socket reference
            new RequestProcessor(socket);
        }
    }catch(Exception e)
    {
        System.out.println(e);
    }
}
    public static void main(String data[])
    {
        int portNumber = Integer.parseInt(data[0]);
        Server server = new Server(portNumber);
//        System.out.println(ThreadI/);
    }
}