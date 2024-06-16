import NPZ
import Ecp

const FILE_FORMAT = ARGS[1]
const FILE_NUMBER = parse(Int64, ARGS[2])
const FILE_OUT = ARGS[3]

const number_of_steps = (10, 10)

for i in 0:(FILE_NUMBER-1)
    println("Processing $(i)")
    filtration = NPZ.npzread("$(FILE_FORMAT)_$(i).npy")
    contributions = Ecp.compute_contributions_3d(filtration)
    vectorized_ecp = Ecp.vectorize_ecp(contributions, number_of_steps)
    NPZ.npzwrite("$(FILE_OUT)_$(i)", vectorized_ecp)
end