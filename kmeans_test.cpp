#include "dtw.h"

struct Point
{
    double x, y;
} P[1000];

int main()
{
    FILE *fin = fopen("kmeasn_test_data.txt", "r");
    
    int n = 0;
    while (fscanf(fin, " %lf %lf", &P[n].x, &P[n].y) != EOF)
        n++;
    fclose(fin);

    Matrix dist;
    dist.n = dist.m = n;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
        {
            dist.v[i][j] = sqrt((P[i].x - P[j].x) * (P[i].x - P[j].x) + (P[i].y - P[j].y) * (P[i].y - P[j].y));
            //printf("%lf\n", dist.v[i][j]);
        }

    int centers[n], K = 3;
    kmeans(dist, centers, K);

    int cluster[K + 1][n + 1], cnt[K + 1];
    for (int k = 0; k < K; k++)
        cluster[k][0] = centers[k], cnt[k] = 1;
    for (int i = 0; i < n; i++)
    {
        double dist_min = inf;
        int c = 0;
        for (int k = 0; k < K; k++)
            if (dist.v[i][centers[k]] < dist_min)
                dist_min = dist.v[i][centers[k]], c = k;
        cluster[c][cnt[c]++] = i;
    }
    for (int k = 0; k < K; k++)
        printf("%d\n", cnt[k]);

    FILE *fout = fopen("kmeans_test_result.txt", "w");
    for (int k = 0; k < K; k++)
    {
        int p;
        for (int k = 0; k < K - 1; k++)
        {
            p = initc[k];
            fprintf(fout, "%lf %lf,", P[p].x, P[p].y);
        }
        fprintf(fout, "%lf %lf\n", P[initc[K - 1]].x, P[initc[K - 1]].y);

        for (int k = 0; k < K - 1; k++)
        {
            p = centers[k];
            fprintf(fout, "%lf %lf,", P[p].x, P[p].y);
        }
        fprintf(fout, "%lf %lf\n", P[centers[K - 1]].x, P[centers[K - 1]].y);

        for (int i = 0; i < cnt[k] - 1; i++)
        {
            p = cluster[k][i];
            fprintf(fout, "%lf %lf,", P[p].x, P[p].y);
        }
        p = cluster[k][cnt[k] - 1];
        fprintf(fout, "%lf %lf\n", P[p].x, P[p].y);
    }
    fclose(fout);
    return 0;
}