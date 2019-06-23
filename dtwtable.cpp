#include "dtw.h"

int disttable(const vector<Seq> &points, Matrix &dist)
{
    int n = points.size();
    dist.n = dist.m = n;
    for (int i = 0; i < n; i++)
    {
        // printf("row %d\n", i);
        dist.v[i][i] = 0;
        for (int j = 0; j < n; j++)
            dist.v[i][j] = dist.v[j][i] = dtw(points[i], points[j]);
    }
    return n;
}

char dir_in[20] = "features";
char dir_out[20] = "dtw/tables";
Matrix table;

int main(int argc, char **argv)
{
    int start = 0, end = word_num;
    if (argc >= 3)
    {
        start = max(atoi(argv[1]), 0);
        end = min(atoi(argv[2]) + 1, 20);
        cout << start << " " << end - 1 << endl;
    }

    vector<string> students = loads("students.txt");
    char filename[200];
    for (int w = start; w < end; w++)
    {
        sprintf(filename, "%s/%d.csv", dir_out, w);
        FILE *fout = fopen(filename, "w");
        if (fout == NULL)
        {
            printf("Cannot find output path!\n");
            return 0;
        }

        vector<Seq> obseqs;
        for (vector<string>::iterator it = students.begin(); it != students.end(); it++)
            for (int k = 1; k <= 20; k++)
            {
                sprintf(filename, "%s/%s/%s-%02d-%02d.csv", dir_in, it->c_str(), it->c_str(), w, k);
                Seq obseq;
                readcsv<Seq>(obseq, filename);
                obseqs.push_back(obseq);
            }

        int n = disttable(obseqs, table);
        printf("%d\n", n);
        table.print(fout);
        fclose(fout);
    }
    return 0;
}
