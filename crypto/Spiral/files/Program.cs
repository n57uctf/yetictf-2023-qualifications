
namespace Spiral
{
    public class Programm
    {
        public static List<List<int>> coil(string flag)
        {
            List<List<int>> result = new List<List<int>>
            {
                new List<int> {0,0,0,0},
                new List<int> {0,0,0,0},
                new List<int> {0,0,0,0},
                new List<int> {0,0,0,0}
            };
            int[] dx = { -1, 0, 1, 0 };
            int[] dy = { 0, -1, 0, 1 };
            int row = result.Count() - 1;
            int col = result.Count() - 1;
            int k = flag.Length - 1;
            for (int count = 0, i = 0; count <4; count++)
            {
                i = count % 4 ;
                    while (col >= 0 && col < 4 && row >= 0 && row < 4)
                    {
                        result[row][col] = (Convert.ToInt32(flag[k])+6)*5;
                        k--;
                        if (col + dx[i] >= 0 && col + dx[i] < 4)
                            col += dx[i];
                        if (row + dy[i] >= 0 && row + dy[i] < 4)
                            row += dy[i];
                        if (result[row][col] != 0)
                        {
                            if (i + 1 < 4)
                            {
                                col += dx[i+1];
                                row += dy[i+1];
                            }
                            else
                            {
                                col = 2;
                                row = 2;
                                for(i = 0;i < 4;i++)
                                {
                                    result[row][col] = (Convert.ToInt32(flag[k])+6)*5;
                                    k--;
                                    if (col + dx[i] >= 0 && col + dx[i] < 4)
                                        col += dx[i];
                                    if (row + dy[i] >= 0 && row + dy[i] < 4)
                                        row += dy[i];
                                }
                            }
                            break;
                        }
                    }
            }
            return result;
        }

        public static string skitala(string str)
        {
            List<List<char>> matrix= new List<List<char>> 
            {
                new List<char> {'a','a','a','a'},
                new List<char> {'a','a','a','a'},
                new List<char> {'a','a','a','a'},
                new List<char> {'a','a','a','a'}
            };

            for ( int row =0, k  = 0; row<4;row++)
            {
                for (int col =0; col < 4; col++)
                {
                    matrix[row][col] = str[k];
                    k++;
                }
            }
            string result ="";
            for ( int col =0, k  = 0; col<4;col++)
            {
                for (int row =0; row < 4; row++)
                {
                    result += matrix[row][col];
                    k++;
                }
            }
            return result;
        }

        public static List<int> shifertext( List<List<int>> key, List<List<int>> message)
        {
            List<int> result = new List<int>();
            for ( int row =0; row< 4;row++)
            {
                for (int col =0; col < 4; col++)
                {
                    result.Add(key[row][col]^message[row][col]);
                }
            }
            return result;
        }

        public static int Main()
        {
            string flag = "";
            List<List<int>> result_mes = new List<List<int>>();
            result_mes = coil(flag);
            string key = "";
            string key_str = skitala(key);
            List<List<int>> key_result = new List<List<int>>();
            key_result = coil(key_str);
            List<int> result = new List<int>();
            result = shifertext(key_result,result_mes);
            return 1;
        }
    };
}