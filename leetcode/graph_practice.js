let logs = []; 

class UndirectedGraph {
    constructor() {
        this.edges = {};
    }

    addVertex(vertex) {
        this.edges[vertex] = {};
    }
    
    addEdge(vertex1, vertex2, weight) {
        if (weight == undefined) {
            weight = 0;
        }

        this.edges[vertex1][vertex2] = weight;
        this.edges[vertex2][vertex1] = weight;
    }
    
    removeEdge(vertex1, vertex2) {
        if (this.edges[vertex1] && this.edges[vertex1][vertex2] != undefined) {
            delete this.edges[vertex1][vertex2];
        }

        if (this.edges[vertex2] && this.edges[vertex2][vertex1] != undefined) {
            delete this.edges[vertex2][vertex1];
        }
    }
    
    removeVertex(vertex) {
        for (var adjacentVertex in this.edges[vertex]) {
            this.removeEdge(adjacentVertex, vertex);
        }

        delete this.edges[vertex];
    }
}


// var graph1 = new UndirectedGraph();
// graph1.addVertex(1);
// graph1.addVertex(2);
// graph1.addEdge(1, 2, 1);
// graph1.addVertex(3);
// graph1.addVertex(4);
// graph1.addVertex(5); 
// graph1.addEdge(2, 3, 8);
// graph1.addEdge(3, 4, 10);
// graph1.addEdge(4, 5, 100);
// graph1.addEdge(1, 5, 88); 

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

function _is_empty(obj) {
    return Object.keys(obj).length === 0; 
}

function _extract_min(Q, dist) {
    var minimum_distance = Infinity,
        node_with_minimum_distance = null; 

    for(var node in Q) {
        if (dist[node] < minimum_distance) {
            minimum_distance = dist[node];
            node_with_minimum_distance = node; 
        }
    }

    return node_with_minimum_distance; 
}

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
    
    removeVertex(vertex) {
        for (var adjacentVertex in this.edges[vertex]) {
            this.removeEdge(adjacentVertex, vertex);
        }

        delete this.edges[vertex];
    }

    removeEdge(originVertex, destVertex) {
        if (this.edges[originVertex] && this.edges[originVertex][destVertex] != undefined) {
            delete this.edges[originVertex][destVertex];
        }
    }

    bfs(vertex) {
        var queue = [], visited = {}; 

        queue.push(vertex); 

        while (queue.length) {
            vertex = queue.shift();
            if (!visited[vertex]) {
                visited[vertex] = true; 
                logs.push(vertex); 
                for (var adjacent_vertex in this.edges[vertex]) {
                    queue.push(adjacent_vertex); 
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
        for(var adjacent_vertex in this.edges[vertex]) {
            if (!visited[adjacent_vertex]) {
                this._dfs(adjacent_vertex, visited); 
            }
        }
    }

    dijkstra(source) {
        var Q = {}, dist = {}; 

        for (var vertex in this.edges) {
            dist[vertex] = Infinity; 
            Q[vertex] = this.edges[vertex]; 
        }
        dist[source] = 0

        while(!_is_empty(Q)) {
            var u = _extract_min(Q, dist); 

            delete Q[u]; 

            for (var neighbor in this.edges[u]) {
                var alt = dist[u] + this.edges[u][neighbor]; 
                if (alt < dist[neighbor]) {
                    dist[neighbor] = alt; 
                }
            }
        }

        return dist; 
    }

    topo_sort_util(v, visited, stack) {
        // this part is not in book because he made a fucking mistake 🤬
        visited[v] = v; 

        for (var item in this.edges[v]) {
            if(visited.hasOwnProperty(item) == false) {
                this.topo_sort_util(item, visited, stack);
            }
        }
        stack.unshift(v); 
    }

    topo_sort() {
        var visited = {}, stack = []; 

        for (var item in this.edges) {
            if (visited.hasOwnProperty(item) == false) {
                this.topo_sort_util(item, visited, stack); 
            }
        }

        return stack; 
    }
}


var dg_topo = new DirectedGraph();
dg_topo.addVertex('A');
dg_topo.addVertex('B');
dg_topo.addVertex('C');
dg_topo.addVertex('D');
dg_topo.addVertex('E');
dg_topo.addVertex('F');
dg_topo.addEdge('B', 'A');
dg_topo.addEdge('D', 'C');
dg_topo.addEdge('D', 'B');
dg_topo.addEdge('B', 'A');
dg_topo.addEdge('A', 'F');
dg_topo.addEdge('E', 'C');
var topo_order = dg_topo.topo_sort();
console.log(dg_topo); 
console.log(topo_order); 

// var dgraph1 = new DirectedGraph();
// dgraph1.addVertex("A");
// dgraph1.addVertex("B");
// dgraph1.addVertex("C");
// dgraph1.addVertex("D");
// dgraph1.addVertex("E"); 
// dgraph1.addEdge("A", "B", 1);
// dgraph1.addEdge("B", "C", 1);
// dgraph1.addEdge("C", "A", 1);
// dgraph1.addEdge("C", "E", 1);
// dgraph1.addEdge("C", "D", 1);
// dgraph1.addEdge("A", "D", 1); 
// dgraph1.addEdge("D", "E", 1); 
// - BREADTH -
// dgraph1.bfs("B"); 
// logs.push(dgraph1.dijkstra("A").toString()); 

// var dgraph1b = new DirectedGraph();
// dgraph1b.addVertex("A");
// dgraph1b.addVertex("B");
// dgraph1b.addVertex("C");
// dgraph1b.addVertex("D");
// dgraph1b.addVertex("E");
// dgraph1b.addVertex("F");
// dgraph1b.addVertex("G");
// dgraph1b.addVertex("H");
// dgraph1b.addVertex("i");
// dgraph1b.addVertex("j");
// dgraph1b.addVertex("k");
// dgraph1b.addEdge("A", "B");
// dgraph1b.addEdge("B", "C");
// dgraph1b.addEdge("B", "E");
// dgraph1b.addEdge("B", "j");
// dgraph1b.addEdge("B", "k");
// dgraph1b.addEdge("C", "D");
// dgraph1b.addEdge("D", "G");
// dgraph1b.addEdge("D", "F");
// dgraph1b.addEdge("G", "H");
// dgraph1b.addEdge("F", "i");
// BREADTH
// dgraph1b.bfs("A"); 
// DEPTH 
// dgraph1b.dfs("A"); 

// var dgraph2 = new DirectedGraph();
// dgraph2.addVertex(1);
// dgraph2.addVertex(2);
// dgraph2.addEdge(1, 2, 1);
// dgraph2.addVertex(3);
// dgraph2.addVertex(4);
// dgraph2.addVertex(5);
// dgraph2.addEdge(2, 3, 8);
// dgraph2.addEdge(3, 4, 10);
// dgraph2.addEdge(4, 5, 100);
// dgraph2.addEdge(1, 5, 88);
// DEPTH 
// dgraph2.dfs(1)


const out = document.getElementById("output");
function println(...args) {
  out.textContent += args.join(" ") + "\n";
}
// println("BFS order:\n");
println(logs.join(" -> "));





//