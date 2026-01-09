                        Action Client = Manager
                        Action Server = Worker



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

RUNTIME PHASE (happens per goal)

4️⃣ A goal arrives
5️⃣ Server reads goal data
6️⃣ Server starts work (loop / long task)
7️⃣ Server sends feedback while working
8️⃣ Server checks: “Has client cancelled?”
9️⃣ Server finishes work
🔟 Server sends final result




When a client sends a goal, execute_callback() runs.
Inside it, the server must:

Acknowledge the goal

Read goal data

Perform the long-running work

Periodically send feedback

Continuously check for cancellation

Finish by returning a result (success / cancel / abort)

That’s it.







 ACTION CLIENT:

Client’s job is NOT to do work.

Client only:

Sends goal

Listens to feedback

Waits for result

CLIENT REQUIRED PARTS (NON-NEGOTIABLE)

Node

ActionClient

wait_for_server()

Goal object

send_goal_async()

goal_response_callback

result_callback

spin()

🧠 THE ACTION CLIENT FLOW (THIS IS THE CORE)

This flow never changes, no matter how complex the robot is:

Node starts
↓
Client waits for action server
↓
Client sends goal
↓
Server accepts goal
↓
Client receives feedback (optional, many times)
↓
Server finishes
↓
Client receives result
↓
Client decides what to do next


🔥 This flow is the truth.
Code just implements this flow.



NOW: MAP FLOW → CODE BLOCKS (NO SYNTAX)
1️⃣ Create the client

Meaning:

“I want to talk to an action server.”

2️⃣ Wait for server

Meaning:

“Don’t send goal until server exists.”

Why?
Because ROS nodes start independently.

3️⃣ Create goal

Meaning:

“This is the task I want done.”

Goal object is just data, nothing more.

4️⃣ Send goal asynchronously

Meaning:

“Start the task, don’t block my node.”

ROS is event-driven, never blocking.

5️⃣ Goal response callback

Meaning:

“Did the server accept or reject my goal?”

Server can say NO.

6️⃣ Feedback callback

Meaning:

“Tell me how much work is done so far.”

Optional but powerful.

7️⃣ Result callback

Meaning:

“The task is finished. Here is the final outcome.”



