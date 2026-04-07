# Fish Flocking & Predator Simulation

This project contains two interactive web-based simulations designed to demonstrate emergent flocking behavior using autonomous agent-based AI. The primary file is `fish_sim.html`, which implements an advanced iteration of Craig Reynolds' classic Boids algorithm.

## 1. Core Boids Rules

The fish agents (prey) do not follow predefined paths. Instead, they exhibit complex, life-like schooling behaviors driven by rules computed purely from their local surroundings:

- **Separation (Avoid Crowding):** Fish steer away from neighbors within a very short radius. This prevents the school from collapsing into a single dense point and colliding with one another.
- **Alignment (Match Direction):** Fish look at their flock-mates within a medium perception radius and gently steer to match their average velocity (speed and heading). This allows the flock to move cohesively in one direction.
- **Cohesion (Stick Together):** Fish calculate the center of mass (average position) of all neighbors within their perception radius and steer toward it. This pulls stragglers into the main body of the school.
- **Predator Avoidance (Fleeing):** An overriding repulsive force. If a predator enters a fish's perception radius, the fish aggressively steers in the opposite direction. 

## 2. The Simulation Loop & Iterative Physics

The simulation utilizes the browser's `requestAnimationFrame` to run an endless `loop()` at targeting 60 frames per second. Each frame, the simulation calculates movements using an **Euler integration** approach based on Newtonian physics concepts.

1. **Resetting Forces:** At the start of every frame, the agent's `acceleration` vector is zeroed out.
2. **Calculating Desires:** The Boids algorithms calculate the desired steering vectors (Separation, Alignment, Cohesion) and scale them based on the weights prescribed in the UI.
3. **Applying Force:** These vectors are passed iteratively into `applyForce(f)`, which accumulates them into the agent's `acceleration` vector.
4. **Updating Velocity & Position:** Finally, the `update()` method is called:
   - `velocity = velocity + acceleration`
   - The velocity is clamped using `velocity.limit(maxSpeed)` to ensure the agents don't break speed caps.
   - `position = position + velocity`
5. **Wrap-Around:** If the updated position exceeds the canvas boundaries, the agent's position wraps around to the opposite side (a toroidal space), simulating an infinite ocean.

By translating behavioral intentions into mathematical forces rather than directly moving the X/Y coordinates, the fish display inertia, momentum, and smooth banking turns rather than robotic, instantaneous direction snapping.

## 3. Predator AI & Agglomerative Clustering

In the advanced iteration (`fish_sim.html`), the predator (Shark) uses a mathematically advanced method to hunt. Rather than blindly chasing the closest stray fish, it targets the densest *school* of fish.

It handles this using an $O(N^2)$ **Single-Linkage Agglomerative Clustering** technique driven by a Disjoint Set Union (DSU) graph.
- Every frame, the predator evaluates the distance between all active fish.
- Any fish clustered mathematically close together (e.g. within 60 pixels) are conceptually "linked". 
- The DSU efficiently merges these linked fish into contiguous clusters.
- The system calculates the centroid (Center of Mass) for each isolated cluster.
- The predator evaluates a dynamically weighted score for all centroids, calculated as `distance / sqrt(cluster_size)`. This biases the predator to aggressively hunt large, dense schools even if they are slightly further away than a lone stray fish.
- The predator then steers directly toward this mathematical pivot rather than a physical agent (visibly marked by a faint red crosshair during the simulation).

## 4. Using the Simulator (UI Guide)

The sidebar provides real-time controls over the environment without needing to pause or refresh the simulation.

**Simulation State**
- **50 Fish / Predator:** Injects new agents into the canvas at random coordinates.
- **Clear:** Wipes the canvas of all entities.
- **Presentation:** Hides the UI panels and expands the canvas to fill the screen with a stylized deep water mode. Press `ESC` to exit.

**Features**
- **Predators Eat Fish:** When toggled on, fish visually disappear and are removed from the global state when a predator's hit-circle overlaps them. When off, predators act like shepherds, endlessly chasing fish without depleting the population.
- **Limited FOV:** Realistic sensory occlusion. Fish have a 90-degree blindspot directly behind them, meaning they might not react to a predator tailing them perfectly.
- **Target Clusters:** Toggles the Agglomerative Clustering target AI for the predators.Predators will just target the fish with the nearest euclidean distance.

**Flocking Weights**
- **Separation / Alignment / Cohesion:** Adjusts the multiplier scaling for the core Boid vectors. Cranking Cohesion high and Separation low results in tight blobs, while cranking Separation creates sparse, chaotic schools.
- **Predator Fear Response:** Dictates how strongly the fish repulse from the predator.
- **Panic Contagion:** Multiplier for the "panic ripple". When one fish spots a predator, it enters a sprint state. Neighbors observe this sprinting velocity and synthetically enter a panic state as well, allowing shockwaves to organically ripple across the entire flock before the predator is even in range.
- **Organic Noise:** Introduces a tiny stochastic vector to the acceleration, giving the school a natural "wriggle" so their paths feel less rigidly algorithmic.

## 5. `fish_sim.html` vs  `fish_sim_simple.html`

The project was divided into two distinct files to demonstrate the difference between baseline algorithms and more advanced game AI.

**The "Simple" Version (`fish_sim_simple.html`)**
- Implements only the foundational rules: Separation, Alignment, Cohesion, and Fleeing.
- The predator hunts the absolute closest physical fish regardless of flock density.
- Senses are unrestricted: Fish have a complete 360-degree perception radius of everything around them.
- Serves as the pure mathematical baseline of Reynolds’ original paper.

**The "Pro" Version (`fish_sim.html`)**
- Features the **Agglomerative Clustering** hunt logic.
- Adds realism constraints via **Limited FOV** and **Cruise vs Panic Speeds** (fish prefer jogging at a lower speed to save energy until explicitly threatened).
- Introduces **Panic Contagion (Shockwaves)**. A fish doesn't wait to see a predator; it reacts to the state of the fish next to it, making the flock act as a single reactive super-organism.
- Visuals for presentation mode when we have to do the poster presentation.
