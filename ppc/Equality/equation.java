import java.util.ArrayList;
import java.util.Random;

public class equation {
    private long a;
    private long x;
    private long p;
    private long b;
    public String equation;

    long xGet(){
        return x;
    }
    equation(){
        Random r = new Random();
        int [] prost = {100003, 100019, 100043, 100049, 100057, 100069, 100103, 100109, 100129, 100151, 100153, 100169, 100183, 100189, 100193, 100207, 100213, 100237, 100267, 100271, 100279, 100291, 100297, 100313, 100333, 100343, 100357, 100361, 100363, 100379, 100391, 100393, 100403, 100411, 100417, 100447, 100459, 100469, 100483, 100493, 100501, 100511, 100517, 100519, 100523, 100537, 100547, 100549, 100559, 100591, 100609, 100613, 100621, 100649, 100669, 100673, 100693, 100699, 100703, 100733, 100741, 100747, 100769, 100787, 100799, 100801, 100811, 100823, 100829, 100847, 100853, 100907, 100913, 100927, 100931, 100937, 100943, 100957, 100981, 100987, 100999, 101009, 101021, 101027, 101051, 101063, 101081, 101089, 101107, 101111, 101113, 101117, 101119, 101141, 101149, 101159, 101161, 101173, 101183, 101197, 101203, 101207, 101209, 101221, 101267, 101273, 101279, 101281, 101287, 101293, 101323, 101333, 101341, 101347, 101359, 101363, 101377, 101383, 101399, 101411, 101419, 101429, 101449, 101467, 101477, 101483, 101489, 101501, 101503, 101513, 101527, 101531, 101533, 101537, 101561, 101573, 101581, 101599, 101603, 101611, 101627, 101641, 101653, 101663, 101681, 101693, 101701, 101719, 101723, 101737, 101741, 101747, 101749, 101771, 101789, 101797, 101807, 101833, 101837, 101839, 101863, 101869, 101873, 101879, 101891, 101917, 101921, 101929, 101939, 101957, 101963, 101977, 101987, 101999, 102001, 102013, 102019, 102023, 102031, 102043, 102059, 102061, 102071, 102077, 102079, 102101, 102103, 102107, 102121, 102139, 102149, 102161, 102181, 102191, 102197, 102199, 102203, 102217, 102229, 102233, 102241, 102251, 102253, 102259, 102293, 102299, 102301, 102317, 102329, 102337, 102359, 102367, 102397, 102407, 102409, 102433, 102437, 102451, 102461, 102481, 102497, 102499, 102503, 102523, 102533, 102539, 102547, 102551, 102559, 102563, 102587, 102593, 102607, 102611, 102643, 102647, 102653, 102667, 102673, 102677, 102679, 102701, 102761, 102763, 102769, 102793, 102797, 102811, 102829, 102841, 102859, 102871, 102877, 102881, 102911, 102913, 102929, 102931, 102953, 102967, 102983, 103001, 103007, 103043, 103049, 103067, 103069, 103079, 103087, 103091, 103093, 103099, 103123, 103141, 103171, 103177, 103183, 103217, 103231, 103237, 103289, 103291, 103307, 103319, 103333, 103349, 103357, 103387, 103391, 103393, 103399, 103409, 103421, 103423, 103451, 103457, 103471, 103483, 103511, 103529, 103549, 103553, 103561, 103567, 103573, 103577, 103583, 103591, 103613, 103619, 103643, 103651, 103657, 103669, 103681, 103687, 103699, 103703, 103723, 103769, 103787, 103801, 103811, 103813, 103837, 103841, 103843, 103867, 103889, 103903, 103913, 103919, 103951, 103963, 103967, 103969, 103979, 103981, 103991, 103993, 103997, 104003, 104009, 104021, 104033, 104047, 104053, 104059, 104087, 104089, 104107, 104113, 104119, 104123, 104147, 104149, 104161, 104173, 104179, 104183, 104207, 104231, 104233, 104239, 104243, 104281, 104287, 104297, 104309, 104311, 104323, 104327, 104347, 104369, 104381, 104383, 104393, 104399, 104417, 104459, 104471, 104473, 104479, 104491, 104513, 104527, 104537, 104543, 104549, 104551, 104561, 104579, 104593, 104597, 104623, 104639, 104651, 104659, 104677, 104681, 104683, 104693, 104701, 104707, 104711, 104717, 104723, 104729, 104743, 104759, 104761, 104773, 104779, 104789, 104801, 104803, 104827, 104831, 104849, 104851, 104869, 104879, 104891, 104911, 104917, 104933, 104947, 104953, 104959, 104971, 104987, 104999 };
        a = r.nextInt(100000)+10000;
        p = prost[r.nextInt(prost.length-1)];
        b = a;
        while(b >= a){b = r.nextInt(100000)+10000;}
        x = this.shag(this.a, this.b, this.p);
        equation = ("a = " + ((Long) a).toString() +  " b = " + ((Long) b).toString() + " p = " + ((Long) p).toString());
    }
//    public static int find_x(int a, int b, int p){
//        int f = 1;
//        int  x = 0;
//        while(f!=b){
//            f *= a;
//            f %= p;
//            x++;
//        }
//        return x;
//    }
public static long mod(long a, long deg, long p){
    long b = 1;
    while(deg != 0){
        b = b * a;
        b = b % p;
        deg--;
    }
    return b;
}
    public static long shag(long a, long b, long p){
        int m, k;
        m = k = (int)(Math.sqrt(p))+1;
        int x;
        ArrayList<Long> a_deg = new ArrayList<>();
        ArrayList<Long> b_deg = new ArrayList<>();
        for(int i = 1; i < k+1; i++){
            a_deg.add(mod(a, i*m, p));
        }
        for(int i = 0; i < m; i++){
            b_deg.add(b*mod(a, i, p)%p);
        }
        int i = 0;
        int j = 0;
        for(i = 0; i < k; i++){
            for(j = 0; j < m; j++){
                if(a_deg.get(i).equals(b_deg.get(j))){
                    break;
                }
            }
            if(j != m && a_deg.get(i).equals(b_deg.get(j))){
                i++;
                break;
            }
        }
        x = i*m-j;
        return x;
    }


}
