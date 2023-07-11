\ Model MCBM
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  f
Subject To
 s: x[s,1] + x[s,2] + x[s,3] + x[s,4] + x[s,5] - f = 0
 t: - x[7,t] - x[8,t] - x[9,t] - x[6,t] - x[10,t] + f = 0
 -[1]: - x[s,1] + x[1,7] + x[1,8] = 0
 -[2]: - x[s,2] + x[2,7] + x[2,8] + x[2,9] = 0
 -[3]: - x[s,3] + x[3,6] + x[3,7] + x[3,8] + x[3,10] = 0
 -[4]: - x[s,4] + x[4,8] = 0
 -[5]: - x[s,5] + x[5,8] + x[5,9] + x[5,10] = 0
 -[6]: - x[3,6] + x[6,t] = 0
 -[7]: - x[1,7] - x[2,7] - x[3,7] + x[7,t] = 0
 -[8]: - x[1,8] - x[2,8] - x[3,8] - x[4,8] - x[5,8] + x[8,t] = 0
 -[9]: - x[2,9] - x[5,9] + x[9,t] = 0
 -[10]: - x[3,10] - x[5,10] + x[10,t] = 0
Bounds
Binaries
 x[s,1] x[s,2] x[s,3] x[s,4] x[s,5] x[1,7] x[1,8] x[2,7] x[2,8] x[2,9]
 x[3,6] x[3,7] x[3,8] x[3,10] x[4,8] x[5,8] x[5,9] x[5,10] x[7,t] x[8,t]
 x[9,t] x[6,t] x[10,t]
Generals
 f
End
