% Use this editor as a MiniZinc scratch book


int: n;
set of int: CURR = 1..n;

int: num_semestres;
set of int: SEMESTRES = 1..num_semestres;

array[CURR] of int: creditos;

var int: energia_no_vacios;
var int: energia_balance;
var int: energia_low;
var int: energia_stability;

int: target_creditos;
int: w_no_vacios;
int: w_balance;
int: w_low;
int: min_load;
int: w_stability;

int: total_relaciones = n * n;
set of int: REL = 1..total_relaciones;

array[REL] of bool: prereq_flat;
array[REL] of bool: coreq_flat;

array[CURR, CURR] of bool: prereq =
  array2d(CURR, CURR, prereq_flat);

array[CURR, CURR] of bool: coreq =
  array2d(CURR, CURR, coreq_flat);

array[CURR] of var SEMESTRES: semestre;

array[SEMESTRES] of var int: carga =
  [ sum(m in CURR)(
      bool2int(semestre[m] = s) * creditos[m]
    )
  | s in SEMESTRES
  ];

constraint
  forall(i, j in CURR)(
    prereq[i,j] -> semestre[i] < semestre[j]
  );

constraint
  forall(i, j in CURR)(
    coreq[i,j] -> semestre[i] = semestre[j]
  );

constraint
  forall(i, j in CURR)(
    prereq[i,j] /\ coreq[i,j] -> false
  );

constraint
  forall(i, j in CURR)(
    coreq[i,j] -> coreq[j,i]
  );

constraint true; % (placeholder limpio)

energia_no_vacios =
  sum(s in SEMESTRES)(
    bool2int(carga[s] = 0)
  );

energia_balance =
  sum(s in SEMESTRES)(
    abs(carga[s] - target_creditos)
  );

energia_stability =
  sum(s1 in SEMESTRES, s2 in SEMESTRES where s1 < s2)(
    abs(carga[s1] - carga[s2])
  );  

energia_low =
  sum(s in SEMESTRES)(
    if carga[s] < min_load
    then (min_load - carga[s])
    else 0
    endif
  );

solve minimize (
  w_balance * energia_balance +
  w_low * energia_low +
  w_no_vacios * energia_no_vacios +
  w_stability * energia_stability
);

output [
  "semestre = " ++ show(semestre) ++ "\n",
  "carga = " ++ show(carga) ++ "\n"
];