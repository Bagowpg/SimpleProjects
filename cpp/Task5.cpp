#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <set>



using namespace std;

vector < vector<vector<int>>> corr; // описание коридоров
vector<int> numP; // номера площадок
int N, M, K; // площадки, коридоры, друзья


int Dijkstra()
{
	vector<vector<int>> par(N);
	vector<int> d(N, 99999);
	d[0] = 0;
	set<int> Q;
	Q.insert(0);

	while (Q.size()) {
		set<int>::iterator it = Q.begin();
		int u = *it;
		for (; it != Q.end(); it++)
		{
			if (d[u] > d[*it])
			{
				u = *it;
			}
		}
		Q.erase(u);

		for (int i = 0; i < corr[u].size(); i++)
		{
			int v = corr[u][i][0];
			if (d[v] > d[u] + corr[u][i][1])
			{
				d[v] = d[u] + corr[u][i][1];
				Q.insert(v);
				par[v] = { u };
			}
			else
			{
				if (d[v] == d[u] + corr[u][i][1])
				{
					par[v].push_back(u);
				}
			}
		}
	}


	vector<int> d2(N, 0);
	for (int i = 0; i < K; i++)
	{
		vector<int> color(N, 0);
		vector<int> Q;
		Q.push_back(numP[i]);
		d2[numP[i]]++;
		while (Q.size()) {
			int u = Q[0];

			for (int i = 0; i < par[u].size(); i++)
			{
				int v = par[u][i];
				if (color[v] == 0)
				{
					Q.push_back(v);
					d2[v]++;
					color[v] = 1;
				}
			}
			Q.erase(Q.begin());
		}
	}

	int max = 0;
	for (int i = 0; i < N; i++)
	{
		if ((d2[i] == K) && max < d[i])
		{
			max = d[i];
		}
	}
	return max;
}



void makeGraph(){
	ifstream file;
	ifstream ifs("input.txt");
	cin.rdbuf(ifs.rdbuf());
	cin >> N >> M >> K;


	numP.resize(K);
	for (int i = 0; i < K; i++)
	{
		cin >> numP[i];
	}

	corr.resize(N);

	for (int i = 0; i < M; i++)
	{
		int u, v, weight;
		cin >> u >> v >> weight;
		corr[u].push_back({ v,weight });
		corr[v].push_back({ u,weight });
	}
}
int main()
{
	setlocale(LC_ALL, "Russian");

	
	//file.open("input.txt");

	makeGraph();


	cout << Dijkstra();

	return 0;
}


