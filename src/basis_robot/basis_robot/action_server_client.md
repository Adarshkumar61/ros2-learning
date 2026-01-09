WHAT THE ACTION SERVER DOES (NO CODE)


“When a goal comes, the server:

Reads the target number

Starts counting from 1

After each count:

sends feedback

waits a bit

When finished:

marks success

sends result”

This description IS the code.
Python just translates it.

🧠 WHAT PARTS WILL DEFINITELY EXIST IN SERVER CODE?

These are NON-NEGOTIABLE:

ActionServer

execute_callback(goal_handle)

Read goal → goal_handle.request

Feedback object

publish_feedback()

succeed()

Return Result

spin()

If any one is missing → broken action.