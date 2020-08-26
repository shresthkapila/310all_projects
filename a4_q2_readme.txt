My KB file (a4_q2_kb.txt) include rules of different topics specified on line 1 of the KB file
     (i.e topics <-- weather & sports & seasons & diseases)
So the rules depend on topics => weather(from assignment)
                              => seasons
                              => sports
                              => diseases

The user can add as much features( rules ) to above topics and example is shown below:


 50 new rules(s) added
kb> tell corona_virus
        "corona_virus" added to KB
kb> infer_all
        Newly inferred atoms:
           infected
        Atoms already known to be true:
           corona_virus
kb> infer_all
        Newly inferred atoms:
           <none>
        Atoms already known to be true:
           corona_virus, infected
kb> tell outdoor
        "outdoor" added to KB
kb> tell running
        "running" added to KB
kb> infer_all
        Newly inferred atoms:
           <none>
        Atoms already known to be true:
           corona_virus, infected, outdoor, running
kb> tell healthyfood
        "healthyfood" added to KB
kb> infer_all
        Newly inferred atoms:
           goodhealth
        Atoms already known to be true:
           corona_virus, infected, outdoor, running, healthyfood
kb> infer_all
        Newly inferred atoms:
           <none>
        Atoms already known to be true:
           corona_virus, infected, outdoor, running, healthyfood, goodhealth
kb> 