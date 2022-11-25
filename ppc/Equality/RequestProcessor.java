import java.io.*;
import java.net.*;
import java.security.spec.RSAOtherPrimeInfo;
import java.util.ArrayList;
import java.util.Random;

class RequestProcessor extends Thread //for multi-threaded server
{
    private Socket socket;
    RequestProcessor(Socket socket)
    {
        this.socket=socket;
        start(); // will load the run method
    }
    public void run()
    {
        try {
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            String x = "We will send you equation type of a^x = b mod p \n";
            String y;
            equation eq;
            int i = 0;
            int n = 0;
            out.write(x);
            long time;
            while (true) {
                eq = new equation();
                time = System.currentTimeMillis();
                while(System.currentTimeMillis() - time < 3000);
                out.write(eq.equation + "\n");
                out.flush();
                n++;
                System.out.println(eq.equation);
                System.out.println("I'm listening");
                time = System.currentTimeMillis();
//                Thread.sleep(3001);
                if((y = in.readLine()) != null){
                    System.out.println(y);
                    if(Integer.parseInt(y) == eq.xGet() && System.currentTimeMillis() - time <= 3003){
                        i++;
                        System.out.println("True");
                    }
                    else{
                        i = 0;
                        System.out.println("Answer is wrong or time is over, bye\n");
                        out.write("Answer is wrong or time is over, bye\n");
                        out.flush();
                        out.close();
                        in.close();
                        socket.close();
                    }
                }
                if (n != 10 && i == 10){
                    n = 0;
                    System.out.println("No answer\n");
                    out.write("No answer\n");
                    out.flush();
                    out.close();
                    in.close();
                    socket.close();
                }
                if(n == 10 && i == 10){
                    out.write("YetiCTF{be3r_1s_go0d,_but_cola_is_pr1celess}\n");
                    out.flush();
                    out.close();
                    in.close();
                    socket.close();
                }
            }
        } catch (IOException ioException) {
            ioException.printStackTrace();
        }
    }
}