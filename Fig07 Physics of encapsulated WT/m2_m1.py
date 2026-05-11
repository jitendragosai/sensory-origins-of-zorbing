import numpy as np
from collections import deque

def generate_lattice(L, p):
    return (np.random.rand(L, L) < p).astype(int)

#--- Square lattice neighbours-------
def get_neighbors(i, j, L):
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < L and 0 <= nj < L:
            yield ni, nj

def find_clusters(lattice):
    L = lattice.shape[0]
    visited = np.zeros_like(lattice, dtype=bool)
    cluster_sizes = []

    for i in range(L):
        for j in range(L):
            if lattice[i, j] == 1 and not visited[i, j]:
                queue = deque([(i, j)])
                visited[i, j] = True
                size = 0

                while queue:
                    x, y = queue.popleft()
                    size += 1
                    for nx, ny in get_neighbors(x, y, L):
                        if lattice[nx, ny] == 1 and not visited[nx, ny]:
                            visited[nx, ny] = True
                            queue.append((nx, ny))

                cluster_sizes.append(size)

    return cluster_sizes

def largest_two_clusters(cluster_sizes):
    if len(cluster_sizes) == 0:
        return 0, 0
    if len(cluster_sizes) == 1:
        return cluster_sizes[0], 0

    sorted_sizes = sorted(cluster_sizes, reverse=True)
    return sorted_sizes[0], sorted_sizes[1]


# ---------------- PARAMETERS ----------------
L_list = [20, 40, 60]
p_list = np.linspace(0.55, 0.65, 11)
nsamples = 50

output_file = "m1_m2_with_errors.dat"


# ---------------- MAIN LOOP ----------------
with open(output_file, "w") as f:
    f.write("# L p <m1> err_m1 <m2> err_m2 <m2/m1> err_ratio\n")

    for L in L_list:
        for p in p_list:

            m1_list = []
            m2_list = []
            ratio_list = []

            for _ in range(nsamples):
                lattice = generate_lattice(L, p)
                clusters = find_clusters(lattice)
                s1, s2 = largest_two_clusters(clusters)

                m1_list.append(s1)
                m2_list.append(s2)

                if s1 > 0:
                    ratio_list.append(s2 / s1)
                else:
                    ratio_list.append(0)

            m1_arr = np.array(m1_list)
            m2_arr = np.array(m2_list)
            ratio_arr = np.array(ratio_list)

            # means
            m1_avg = np.mean(m1_arr)
            m2_avg = np.mean(m2_arr)
            ratio_avg = np.mean(ratio_arr)

            # standard errors
            m1_err = np.std(m1_arr, ddof=1) / np.sqrt(nsamples)
            m2_err = np.std(m2_arr, ddof=1) / np.sqrt(nsamples)
            ratio_err = np.std(ratio_arr, ddof=1) / np.sqrt(nsamples)

            f.write(f"{L}\t{p:.5f}\t"
                    f"{m1_avg:.6f}\t{m1_err:.6f}\t"
                    f"{m2_avg:.6f}\t{m2_err:.6f}\t"
                    f"{ratio_avg:.6f}\t{ratio_err:.6f}\n")

print("Done. Output written to", output_file)
