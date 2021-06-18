#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <set>

using namespace std;


int flag = 1;
int N;
int power = 0;
int attack = 0;
vector < vector<vector<int>>> graph;


void makeGraph() {
	ifstream file;
	ifstream ifs("input.txt");
	cin.rdbuf(ifs.rdbuf());
	cin >> N;
	vector<int> edges(N);
	graph.resize(N);


	for (int u = 0; u < N; u++)
	{
		graph[u].resize(N + 2);
		int tower, weights;
		cin >> weights >> tower >> edges[u];
		graph[u][N] = { weights, 0 };
		power += weights;

		if (tower)
		{
			graph[u][N + 1] = { 30000, 0 };
		}
	}

	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
		{
			graph[i][j] = { 0,0 };
		}
	}


	for (int u = 0; u < N; u++)
	{
		for (int j = 0; j < edges[u]; j++)
		{
			int v, p;
			cin >> v >> p;
			graph[u][v][0] = p;
		}
	}
}


void Dijkstra()
{
	vector<int> color(N, 0);
	vector<int> par;
	vector<int> d(N+1, 0);
	d[0] = 99999;
	set<int> Q;
	Q.insert(0);
	par.resize(N+1);

	while (Q.size()) {
		set<int>::iterator it = Q.begin();
		int u = *it;
		for (; it != Q.end(); it++)
		{
			if (d[u] <= d[*it])
			{
				u = *it;
			}
		}
		Q.erase(u);
		color[u] = 1;

		for (int v = 0; v < N+1; v++)
		{
			if (graph[u][v][0] != 0)
			{
				int min;
				if (d[u] < graph[u][v][0] - graph[u][v][1])
					min = d[u];
				else
					min = graph[u][v][0] - graph[u][v][1];


				if (min > d[v])
				{
					d[v] = min;
					par[v] = { u };
				}
				if (v != N && color[v] != 1)
					Q.insert(v);
			}
		}
	}

	attack += d[N];

	int v = N;
	while (v)
	{
		int u = par[v];
		graph[u][v][1] += d[N];
		v = u;
	}

	if (d[N] != 0)
		flag = 1;
}


void maxFlow()
{
	while (flag)
	{
		flag = 0;
		Dijkstra();
	}

}


void resNetwork()
{
	if (power != attack)
	{
		cout << -1;
		exit(0);
	}
	attack = 0;
	flag = 1;


	for (int u = 0; u < N; u++)
	{
		for (int v = 0; v < N+2; v++)
		{
			if (v < N)
			{
				//graph[v][u][0] += graph[u][v][1];
				graph[u][v][0] -= graph[u][v][1];
				graph[u][v][1] = 0;
			}
			if ((v == N) && graph[u][v+1].size())
			{
				graph[u][v][0] = graph[u][v + 1][0];
				graph[u][v][1] = 0;
			}
		}
	}
}


int main()
{
	setlocale(LC_ALL, "Russian");


	makeGraph();
	maxFlow();
	resNetwork();
	maxFlow();

	cout << attack;

	return 0;
}


