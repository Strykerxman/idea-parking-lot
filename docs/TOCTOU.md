TOCTOU
------

_What is TOCTOU?_  

**TOCTOU** stands for ***time-of-check to time-of-use***. In the case of the Idea Parking Lot, when a user wants to activate an idea, the app must:  

1. check: there is no other active idea  
3. use: activate the idea  

In TOCTOU, “use” means acting based on the condition you previously checked.  

This is a classic issue because the current app logic uses two seperate transactions to first check the active idea (if any) and then the second transaction sets the idea's status to active. If these happen in two separate transactions, there is a gap between the check and the update.  

For example two requests could both:  

1. check and see no active idea  
2. both pass validation  
3. each activate a different idea  

This could violate the invariant that at most one idea is active.  

For a single-user application, this risk is small, although multiple tabs, double submissions or overlapping requests could still cause it.  

Later in the project development, idea activation may also need to:  

1. save the user's reflection/history  
2. deactivate the old idea  
3. activate the new idea

These changes should happen in a single transaction so that if one of them fails, the whole transaction rolls back.  

The main reason for using one transaction is **atomicity & data consistency**, not performance. Fewer transactions may also reduce database overhead, but that is secondary.  