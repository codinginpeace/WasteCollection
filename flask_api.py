from flask import Flask, request, jsonify
import pandas as pd
from gurobipy import Model, GRB
from mapProcessor.map import get_node_indexing_and_road_distance_matrix
from functions.funct import all_subsets_except_depot


app = Flask(__name__)

def get_outputs(m, depot, K, V, x):
    result = {'status': None, 'objective_value': None, 'routes': []}
    if m.status in [GRB.OPTIMAL, GRB.SUBOPTIMAL]:
        result['status'] = 'success'
        result['objective_value'] = m.objVal
        for k in range(K):
            # Initialize the route with the depot
            route = [depot]
            while True:
                i = route[-1]
                # Find the next node in the route
                next_node = next((j for j in V if i != j and x[i, j, k].X > 0.5), None)
                # If no next node or we're back at the depot, the route is complete
                if next_node is None or next_node == depot:
                    break
                route.append(next_node)
            # Append the final route for vehicle k to the result
            result['routes'].append({'vehicle': k, 'route': route})
    else:
        result['status'] = 'failure'
        result['message'] = "No valid solution found."
    return result

def find_optimal_route(road_distance_matrix, vehicle_capacity, depot, V, N, K, demands, service_times):
    ### MODEL STARTS
    # Create the model
    m = Model("vrp")

    # Create variables
    x = m.addVars([(i, j, k) for i in V for j in V for k in range(K)], vtype=GRB.BINARY, name='x') #1 if vechicle K moves over i to j
    y = m.addVars([(h, k) for h in V for k in range(K)], vtype=GRB.BINARY, name='y') #wether vechicle k visists vertex i

    # Assuming road_distance_matrix is your numpy array of distances
    # Convert the numpy array to a pandas DataFrame
    distances_df = pd.DataFrame(road_distance_matrix, index=V, columns=V)

    # Now, when setting the objective function in your optimization model, use distances_df instead of distances
    m.setObjective(sum(distances_df.loc[i, j] * x[i, j, k] for i in V for j in V for k in range(K)), GRB.MINIMIZE)

    # Constraints
    # Each customer is visited exactly once
    for i in V:  # Exclude the depot
        if i != depot:
            m.addConstr(sum(y[i, k] for k in range(K)) == 1)

    # Number of vehicles leaving the depot
    m.addConstr(sum(y[depot, k] for k in range(K)) == K)

    # Flow conservation constraints
    for i in V:
        for k in range(K):
            m.addConstr(sum(x[i, j, k] for j in V) == sum(x[j, i, k] for j in V))
            m.addConstr(sum(x[i, j, k] for j in V) == y[i, k])

    # Auxiliary variables for MTZ
    u = m.addVars(V, vtype=GRB.CONTINUOUS, name='u')

    # MTZ constraints
    for i in V:
        for j in V:
            if i != depot and j != depot and i != j:
                m.addConstr(u[i] - u[j] + N * x[i, j, k] <= N - 1)

    # Each vehicle's capacity should not exceed the maximum vehicle capacity
    for k in range(K):
        m.addConstr(sum(demands[i] * y[i, k] for i in V) <= vehicle_capacity)

    subsets_within_capacity = all_subsets_except_depot(V, demands, vehicle_capacity)

    # Now add the constraint
    for M in subsets_within_capacity:
        for h in M:
            for k in range(K):
                # You should only sum over i and j if the variable for x[i, j, k] exists
                m.addConstr(sum(x[i, j, k] for i in M for j in V if j not in M and (i, j, k) in x) >= y[h, k])

    # Solve the model
    m.optimize()
    return get_outputs(m, depot, K, V, x)  # Adapt this function to return data instead of writing to Streamlit

@app.route('/optimize', methods=['POST'])
def optimize_route():
    data = request.json
    road_distance_matrix = data['road_distance_matrix']
    vehicle_capacity = data['vehicle_capacity']
    depot = data['depot']
    V = data['V']
    N = data['N']
    K = data['K']
    demands = data['demands']
    service_times = data['service_times']
    
    # Convert the received distance matrix into the format expected by your optimization function
    df = pd.DataFrame(road_distance_matrix, index=V, columns=V)
    
    # Call your optimization function
    result = find_optimal_route(df.values.tolist(), vehicle_capacity, depot, V, N, K, demands, service_times)
    
    # Return the optimization results
    return jsonify(result)

def get_outputs_streamlit(m, depot, K, V, x):
    # Adapt your original function to return data instead of printing or writing to Streamlit
    # Return a dictionary or list that represents your optimization results
    # Example (you need to adjust according to your actual data structure):
    if m.status in [GRB.OPTIMAL, GRB.SUBOPTIMAL]:
        routes = []
        for k in range(K):
            route = [depot]
            while True:
                i = route[-1]
                next_node = next((j for j in V if i != j and x[i, j, k].X > 0.5), None)
                if next_node is None or next_node == depot:
                    break
                route.append(next_node)
            routes.append({'vehicle': k, 'route': route})
        return {'status': 'success', 'routes': routes, 'objective_value': m.objVal}
    else:
        return {'status': 'error', 'message': 'No valid solution found.'}

if __name__ == '__main__':
    app.run(debug=True, port=5001)
