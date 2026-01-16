let logs = []; 

function UndirectedGraph () {
    this.edges = {}
}

UndirectedGraph.prototype.addVertex = function (vertex) {
    this.edges[vertex] = {};
}

UndirectedGraph.prototype.addEdge = function (vertex1, vertex2, weight) {
    if (weight == undefined) {
        weight = 0
    }

    this.edges[vertex1][vertex2] = weight;
    this.edges[vertex2][vertex1] = weight;
}

UndirectedGraph.prototype.removeEdge = function(vertex1, vertex2) {
    if (this.edges[vertex1] && this.edges[vertex1][vertex2] != undefined) {
        delete this.edges[vertex1][vertex2];
    }

    if (this.edges[vertex2] && this.edges[vertex2][vertex1] != undefined) {
        delete this.edges[vertex2][vertex1]; 
    }
}

UndirectedGraph.prototype.removeVertex = function (vertex) {
    for (var adjacentVertex in this.edges[vertex]) {
        this.removeEdge(adjacentVertex, vertex); 
    }

    delete this.edges[vertex]; 
}

var graph1 = new UndirectedGraph();
graph1.addVertex(1);
graph1.addVertex(2);
graph1.addEdge(1, 2, 1);
graph1.addVertex(3);
graph1.addVertex(4);
graph1.addVertex(5); 
graph1.addEdge(2, 3, 8);
graph1.addEdge(3, 4, 10);
graph1.addEdge(4, 5, 100);
graph1.addEdge(1, 5, 88); 

// var graph2 = new UndirectedGraph();
// graph2.addVertex(1);
// graph2.addVertex(2);
// graph2.addEdge(1, 2, 1);
// graph2.addVertex(3);
// graph2.addVertex(4);
// graph2.addVertex(5);
// graph2.addEdge(2, 3, 8);
// graph2.addEdge(3, 4, 10);
// graph2.addEdge(4, 5, 100);
// graph2.addEdge(1, 5, 88);
// graph2.removeVertex(5);
// graph2.removeVertex(1);
// graph2.removeEdge(2, 3);

class DirectedGraph {
    constructor() {
        this.edges = {};
    }
    
    addVertex(vertex) {
        this.edges[vertex] = {};
    }
    
    addEdge(originVertex, destVertex, weight) {
        if (weight === undefined) {
            weight = 0;
        }

        this.edges[originVertex][destVertex] = weight;
    }
    
    removeEdge(originVertex, destVertex) {
        if (this.edges[originVertex] && this.edges[originVertex][destVertex] != undefined) {
            delete this.edges[originVertex][destVertex];
        }
    }
    
    removeVertex(vertex) {
        for (var adjacentVertex in this.edges[vertex]) {
            this.removeEdge(adjacentVertex, vertex);
        }

        delete this.edges[vertex];
    }
    
    bfs(vertex) {
        var queue = [], visited = {};

        queue.push(vertex);

        while (queue.length) {
            vertex = queue.shift();
            if (!visited[vertex]) {
                visited[vertex] = true;
                logs.push(vertex);
                for (var adjacentVertex in this.edges[vertex]) {
                    queue.push(adjacentVertex);
                }
            }
        }
    }
    
    dfs(vertex) {
        var visited = {};
        this._dfs(vertex, visited);
    }

    _dfs(vertex, visited) {
        visited[vertex] = true;
        logs.push(vertex);
        for (var adjacentVertex in this.edges[vertex]) {
            if (!visited[adjacentVertex]) {
                this._dfs(adjacentVertex, visited);
            }
        }
    }
}

var digraph1 = new DirectedGraph();
digraph1.addVertex("A");
digraph1.addVertex("B");
digraph1.addVertex("C");
digraph1.addEdge("A", "B", 1);
digraph1.addEdge("B", "C", 2);
digraph1.addEdge("C", "A", 3);
digraph1.addVertex("D");
digraph1.addEdge("B", "D", 2)
// digraph1.bfs("B"); 

var graph2 = new DirectedGraph();
graph2.addVertex(1);
graph2.addVertex(2);
graph2.addEdge(1, 2, 1);
graph2.addVertex(3);
graph2.addVertex(4);
graph2.addVertex(5);
graph2.addEdge(2, 3, 8);
graph2.addEdge(3, 4, 10);
graph2.addEdge(4, 5, 100);
graph2.addEdge(1, 5, 88);
graph2.dfs(1)



// ChatGPT code:
// =======================
// SAMPLE GRAPH (EDIT ME)
// =======================

const out = document.getElementById("output");

function println(...args) {
  out.textContent += args.join(" ") + "\n";
}


// println("BFS order:\n");
println(logs.join(" -> "));





//