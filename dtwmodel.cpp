#include "dtw.h"
#include <random>

char dir_in[20] = "features";
char dir_out[20] = "dtw";
char dir_table[20] = "dtw/tables";
Matrix table;
vector<Seq> word_obseqs_test[word_num];
vector<Seq> models[word_num];

void readtable(Matrix &table, int w, int n)
{
    char filename[200];
    sprintf(filename, "%s/%d.csv", dir_table, w);
    readcsv<Matrix>(table, filename);
    table.n = table.m = n;
}

int main(int argc, char **argv)
{
    int start = 0, end = word_num;
    if (argc >= 3)
    {
        start = max(atoi(argv[1]), 0);
        end = min(atoi(argv[2]) + 1, word_num);
        cout << start << " " << end - 1 << endl;
    }

    time_t t1 = time(NULL);

    vector<string> students = loads("students.txt");
    char filename[200];
    for (int w = start; w < end; w++)
    {
        vector<Seq> obseqs;
        for (vector<string>::iterator it = students.begin(); it != students.end(); it++)
            for (int k = 1; k <= 20; k++)
            {
                sprintf(filename, "%s/%s/%s-%02d-%02d.csv", dir_in, it->c_str(), it->c_str(), w, k);
                Seq obseq;
                readcsv<Seq>(obseq, filename, 1);
                obseqs.push_back(obseq);
            }

        //int n = obseqs.size() - 60;
        int n = obseqs.size();
        int centers[n + 1], K = 5;
        readtable(table, w, n);
        kmeans(table, centers, K, 5000);

        for (int k = 0; k < K; k++)
        {
            sprintf(filename, "%s/%d-%d_all.csv", dir_out, w, k);
            FILE *fout = fopen(filename, "w");
            models[w].push_back(obseqs[centers[k]]);
            obseqs[centers[k]].print(fout);
            fclose(fout);
        }

        printf("model %d finished\n", w);
        word_obseqs_test[w].clear();
        // for (int i = n; i < obseqs.size(); i++)
        //     word_obseqs_test[w].push_back(obseqs[i]);
        int idx[n + 1];
        for (int i = 0; i < n; i++)
            idx[i] = i;
        random_shuffle(idx, idx + n);
        for (int i = 0; i < n / 10; i++)
            word_obseqs_test[w].push_back(obseqs[idx[i]]);
    }

    time_t t2 = time(NULL);

    if (start != 0 or end != word_num)
        return 0;

    int reg[word_num][word_num], cnt = 0, acc = 0;
    memset(reg, 0, sizeof(reg));
    for (int w = 0; w < word_num; w++)
    {
        const vector<Seq> &obseqs = word_obseqs_test[w];
        for (int i = 0; i < obseqs.size(); i++)
        {
            int decision = decide(obseqs[i], models);
            reg[w][decision] += 1;
            cnt += 1;
            if (decision == w)
                acc += 1;
        }
    }

    for (int i = 0; i < word_num; i++)
    {
        for (int j = 0; j < word_num - 1; j++)
            printf("%d,", reg[i][j]);
        printf("%d\n", reg[i][word_num - 1]);
    }
    printf("%lf\n", 1.0 * acc / cnt);

    time_t t3 = time(NULL);

    printf("%ld %ld %lf\n", t2 - t1, t3 - t2, 1.0 * (t3 - t2) / (60 * 20));
    return 0;
}
