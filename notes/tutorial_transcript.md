### Tutorial 1:

What is an AI Agent
the second and last part of this video
let's let's answer the question what is
an AI agent oh and let me tell you this
is not my definition this is the
definition from Harrison chase the
founder of Lang chain which actually he
created this um amazing blog post that
I'm following right now for this
explanation and you should have a look
at it I'm going to put the link in the
description below so what is an AI agent
and so an AI agent is a system that uses
an llm to decide the control flow of an
application so that would be the direct
answer to the question but I think that
is still a bit too Technical and doesn't
tell us much so let's look at the
following comment actually from Andrew
NG which is that rather than arguing
over which work to include or exclude as
being a true AI agent we can acknowledge
that there are different degrees to
which systems can be agentic this is
like with autonomous vehicles there are
different degrees to to which a vehicle
is autonomous so we have the same thing
now with agents or this agentic nature
of an application and I think this table
from harison Chase Post I think sums it
up amazingly and I also added a couple
of notes so let's let's have a look at
it but but to finish up with this
concept of agentic just let's pay
attention to what I have here so a
system is more tic the more an llm
decides how the system can behave and I
think this sentence is key really to
understand what an agentic system is and
I think it's maybe the the sentence that
sums it up that sums everything up but
let's just have a look at the table now
so this table shows the levels of
autonomy of agency that A system can
have right and it's evaluated in levels
from one to six six being just the most
autonomous or the most agentic so those
labels of agency would be the rows in
this table and just let's have a look at
the columns here so we have decide the
output of each step decide which steps
to take and decide what steps are
available to take right so I'll explain
you everything about this with a couple
of examples and you would understand
understand it well so in level number
one we have just a code a typical code
application right so this is an example
here this is just every app that existed
until 2022 until llms started so here
the output of every step is decided by
the programmer by the human right we we
write code and we have conditionals we
have loops and and we have just
functions right but we always know what
is the output right the human has
decided that and also which steps will
continue after that first output that is
also decided by the human and also what
is going to happen in the whole
application is also decided by the human
then we have level two so this is when
we introduce an a LM call into our
application so here we have an app that
uses an llm to do something an example
of this could be something like um a
summarization summarize this text into
this bullet point so the output of this
function of of of this step is going to
be decided by the llm the llm is going
to do this Iz ation so that would be
level two now for level three we
introduced the concept of a chain and a
chain now is just multiple steps in a in
a in in the same workflow right in the
same so sequentially an example of this
could be a rag so a ret augmented
generation which we do a semantic search
Plus for example using internet an
internet search query to enrich even
more the context right so this whole
thing would be um level three now as for
level four we start looking at the
second column now the system of the app
uses an llm to decide what to do and
here for example is AA so AA um so for
AA we have also a router prompt that
decides how um so in which form should
AA anwers should she answer with a with
a message should she answer with an
image or should she answer with with a
with an audio message and that is
decided by an llm next up we have the
the level number five which would be a
state machine and here the difference
would be that we include cycle so and
here the app would cycle until it finds
the solution for a problems so an
example of this could be a text tosql
agent that retries that that that
computes um um a SQL query runs it again
the database and if the answer is um is
wrong or it's not what expected or if it
has an error then it would retry that
right and it would cycle until the agent
says okay this is enough this is the
query or this is the answer to the query
of the user and then it outputs that and
finally we have level six in which we
have a system that is completely
autonomous so that is that one the
output of everything is just decided by
the llm the step to take or which tool
to use is also decided by the llm and
finally the llm or the yeah this whole
application would build its own tools it
would build these whole things that the
the the system would use to sum it up
the answer to what is an agent isn't
really a definition by itself it's just
that that we have to reframe that into
how agentic a system is so that would be
Lesson 1 finishes
all for part one or lesson one of this
course Ava the WhatsApp agent and
remember this course are going to be six
lessons in total that we're going to
post weekly every Wednesday to YouTube
here in my YouTube channel and to Miguel
newsletter so if you want to be notified
when we do so you should subscribe and
hit the notification Bell and as always
I'm going to leave links in the
description below to everything
important that I have mentioned in this
video including the link to the GitHub
repo because this course is open source
you can check the code right now and I
really think you're going to enjoy this
course and you're going to be able to
build really cool WhatsApp agents
bye-bye and see you in the next one

### WhatsApp AI Agent Tutorial 2: Dissecting Ava's Brain | Intro to LangGraph & LangGraph Studio

Ex Machina Face Swap Magic
you want to see something
cool this is where AA was
created
here we have her
mind
fluid
imperfect
[Music]
patterned
Face Swap Intro
chaotic okay first of all how cool was
that intro and did notice that Oscar
isak's character wasn't really looking
like him or is it maybe that we already
look very similar in that movie well if
you want to know how I did that so how I
swap faces both in images and in videos
just let me know in the comments and I
can do a video about that I think it's
really cool but enough with face
swapping for this video let's let's get
started with this lesson so welcome to
Lesson 2 Intro
lesson two of this curse ABA the
WhatsApp agent in today's video we're
going to cover two things at first we're
going to understand what are these
Frameworks for agentic systems or these
agentic Frameworks and I'm going to
explain you here why we chose to build
Ava using langra and then when that's
clear we're going to dissect aa's brain
and we are going to dissect it by doing
three things by looking at this diagram
that Miguel has prepared by doing a code
overview I'm going to show you all the
important parts um that build avas brain
in code so I'm we're going to be looking
at that as well and finally at the end
of this video I'm going to show you how
you can set up lra studio so that you
can run and debug your agent graph which
actually looks like
this so in lesson one we already Define
Agentic Frameworks
what an AI agent is and actually we
concluded that we shouldn't really be
talking about what is a true AI agent we
should be thinking about agentic system
and now for building this kind of
agentic systems you have different
options or different Frameworks and I
think the first distinction that we have
to make is between low code or no code
tools like n8n or flow wise and code
Frameworks like langra or the new a
small agent from haging face and I think
the key difference between these two
groups boils down to one world which is
control because when you have access to
the code to everything that your agent
or your identic system is doing you can
potentially build anything that you want
well that is if you can code it of
No-Code / Low-Code Framworks: n8n, make, flowise, rivet
course but don't get me wrong I think
this low code applications are becoming
very very powerful I've personally seen
not build but seen a lot of amazing
applications built especially on
n8n which is this kind of graph based or
node based architecture that you can
just drag and drop and just connect
different things but as I said you are
limited by
the integration so you have plenty but
yeah you depend on them implementing an
integration for you though I believe as
well that you can inject code so you
really can do a lot of things but again
it's just not the same as having
complete control over the code then you
also have flow wise and ribet which I
think allows for a lot of code injection
so this I think this they come they come
as this low code more than no code and
then you have make which I think doesn't
get to the level of n88 in terms of yeah
complex the workflows that you can build
or the automations that you can build
are I don't think you can create cycles
for example so I think make is more like
an automation platform more than kind of
like an agentic and then on the other
Code Frameworks: LangGraph, smolagents, crewai...
side we have the code Frameworks and
here among on this two we have the ones
that like lra or Qi and pantic for
example that allows for a lot of control
as well for you to really control every
single part of the application or or
then you also have other Frameworks that
have more as abstraction like like Lan
chain or Lama index I personally haven't
used them all and I think you shouldn't
use the mode I think you should just
choose one that you feel that adapts
better to your workflow and the way that
you work and just commit to it and work
on it and I encourage you that if you
are already a coder or if you are not
afraid of learning how to code you
should go for a coding framework okay
Why LangGraph?
now among all these Frameworks why we
chose lra and again I think it comes
back to the same word to control right
and what I mean by control is that lra
allows you to really go low level and it
removes all these abstractions that for
example L chain has but as I have here I
think also the the way the way that is
architected as a graph I think makes a
lot of sense and even though we go low
level I think it is still intuitive to
understand what is happening in the
system another good point for for me was
that of course it integrates nicely with
L chain because they come from the same
company and I am already a fan of L
chain and what I really like about L
chain is just that is platform agnostic
right that I can easily just use this
inference provider work Gro like we use
here but just change it and now use
anthropic or open AI or azour so the one
that I really prefer and finally as a
robust really framework that it is it
allows you to to have streaming
parallelization of different workflows
readymade integration just to make it
easier for you and also
multi-agents now let's put the focus
Ava's Brain Diagram
back on abas or on abas brain and let's
pay attention to what I have here which
is the title of this lesson abas brain
is graph or as M likes to put it abas
brain is youra Lang
graph but also added an asterisk here
which is down here a stateful graph and
I'm going to explain you just in a
couple of seconds what is this but let
us first look at this beautiful diagram
that Miguel has prepared oh and by the
way if you want to get the content from
this lesson in written form you also
have a link to Miguel's news letter Down
Below in the description box and now
coming back to the diagram so what we
have here are different notes and edges
so that is a graph right and let's
review now all these notes or the most
important ones so then later when we go
to the code we understand it even better
so starting from the top we have the
memory struction so this node what it
does is to understand from the message
of the user if there is a key piece of
information that should be remember so
that should be put into the long-term
memory then we have the router node so
the router was one of these agentic
patterns and what it does is to Route uh
the the flow of the application so what
is the next node that should be executed
so that's what we have here as select
workflows right so our router node what
it does is just what it does is just
that AA would decide
autonomously how she will answer to us
will she answer with a voice note will
she answer with a text or will she
answer with an image Noe so that will
depend on the kind of or the flow of the
conversation right so it will depend on
her and we also have another things for
example we have a note to inject context
and to inject memory so that is for
example avas activities because AA has a
daily schedule and also inject those
memories that could be key to form an
answer and finally once one of these
audio text or image notes are executed H
each one with their pertaining um
inference provider right if it's an
audio node we are going to need to
generate the audio with the level UPS if
it's text we just directly run Lama 3.3
and if it's an image node we will
generate an image using together sayi
flax endpoint and finally we will
"stateful" graph
summarize the conversation so that Ava
can handle the context better and now
before we start looking at the code
let's understand this whole stateful
term so as we said AAS brain is just a
graph right so as with any graph um is
composed by nodes and edges but here in
the case of of lra we also have a state
and is this a state the one that handles
all the information that is being shared
and populated in all these different
nodes and this is going to make much
more sense once we look the code I
promise so let's let's do that so now
how is everything that we have discussed
Code Overview: nodes file
uh reflected now in code well let me
tell you I think it's quite
straightforward and probably even simple
to understand so let's pay attention to
the module graph that we have within the
AI companion uh directory which by the
way if you don't know this um this whole
course is open source and it's free of
course and you have the link down below
to to this GitHub repo so yeah go ahead
and clone the repo if you want to follow
this whole thing in your own ID so here
in the module graph now we have
different files for the edges the nodes
the graph and the state so let's have a
look at those so let's start by looking
at the nodes and what we have here are
different functions that would represent
each node and in each function you
should be looking at two things actually
first of all
at the parameter that each function has
the state we're going to be looking at
the state just in a couple of seconds
but we have just our own panti class the
AI companion state right or avas state
and also the return type so what we have
is a dictionary and this dictionary is
the one that is going to be modifying
the state again you will understand just
in a couple of seconds once we look at
the state and here we have all those
notes that we commented before right so
the image node would be the one that
would create an image and it would
answer H depending on on just the whole
conversation we also have the audio that
would use use 11 labs and we have the
summarized conversation the memory
exraction so we have it all and you
should have a look at The Code by
yourself and just understand it dig deep
just get and and understand every
Code Overview: router node
function but I think in this video maybe
we can look at the router note which is
just the one that I mentioned before
right this identic pattern that what it
does is just to to determine what to do
right so it determines the flow of the
application and what we have is actually
something very very simple so we
actually have just a couple of lines of
of code and what we do is we build a
chain and we build this Chain by just
using a prom that I will show you in a
second with the ex structor output right
so this and and that output is going to
be this class the router response which
which we have over here and this
indicates the model how to resp so what
we have is the response type which
already the name kind of tells what it
is right which kind of response should
ABA give and we give a description just
telling what it is to the model and this
works well because we have the router
prompt and this is just a router prom
that you should have a look at it by
yourself but essentially what we do is
just to really explain to her all the
rules for her to understand when when it
should be an image generation when it
should be an audio
and what are the general the general
rules so I'm not going to read this
whole prom right now you have um you
have it by yourself you can really look
at it and understand why we have done
all these things and now coming back to
the node function right so we have
created that chain that uses the prompt
and that strict our output so now we
have to invoke that chain right with
this invoke asynchronous invoke a
function that gets us the answer and it
is this answer now that we are going to
kind of like plug into the estate by
using this right by
returning this workflow right because
now their workflow is one parameter of
the estate and let's have a look at the
Code Overview: state class
state class right
now and what we have is just a python
class uh that inherits from another
class which is the message messages
State class which allows us to really
try the conversation history and also
keep that last message that we receive
but essentially use a python class you
set up the arguments or the parameters
that you want to be storing and that you
want to be saving and those for us are
these ones right so we have the summary
of the conversation the workflow so this
is just what we have done here right we
decide the workflow based on the router
prompt so we keep that now in the state
same thing also for the audio buff the
image path the current activity and and
the memory and another note that I want
to show you in this video is this
Code Overview: context injection node
context injection note that injects the
context of aa's current activity and I
think this note is quite special because
I think this is part of what makes AA
just act so humanik because she has an
activity she so AA has a schedule and
and we can we can have a look at it and
you can have a look at the The Code by
yourself but essentially what we have is
just kind of like time frame things or
that that she's going to do right for
example she starts a peaceful morning
review in personal machine learning
project results right so and also part
of aa's personality is that she is also
a machine learning engineer like Miguel
and I and this is really cool because
now Miguel and I we can both talk with
ABA about machine Learning Without
boring her so those would be two of the
notes that we have built but as as I
said code this open source just dig deep
into it understand each note by yourself
you're going to really see how
everything makes sense due to this graph
architecture okay so we have seen notes
and the state let's have a look now at
the graph and the edges so we have just
a bit more kind of like complex edges so
this would be conversational edges we
will see that later and we have the
Code Overview: graph file
graph and it is here in this H file
where we put together nodes and edges
and we do that by using the class um
State graph H which uses our um our
state and then what we do is just to
start adding those nodes and then we
connect those nodes via edges right so
we have the kind of like the the start
node that then goes to the memory
extraction node and then we have the
memory extraction note that goes to the
WR or no and we continue to do that
until we have the final graph build
build and the last important element of
L graph that you should understand is
the compilation so once you have that
graph built you have to compile it and
you can compile it using a checkpoint
which actually has a checkpoint of uh
the state and this is what we call the
shortterm memory that we Implement via
SQL L and we are going to explain you
this better in the next lesson along
with the long-term memory that we
Implement using quadrant and finally to
LangGraph Studio Overview
finish up with this video and as
promised in the intro let's have a look
at langra studio so langra studio is a
very powerful app that allows you to
take your graph or your agentic system
that is a graph and allows you to run it
with the state that you want to put so
you can just change anything from the
state for example the a message we can
put something about um what's my
favorite
movie and we can execute this by just
clicking submit or just creating
clicking command
enter and this is going to execute the
graph as it does really right and here
for example we have seen that for giving
us an answer it went on and use the
conversation Noe right so the previous
note was the memory injection and the
next one is the summary conversation
note and for example we can see here the
answer from her which is X minina right
because this is something that I have
told her um in previous conversation so
she knows that right so H look at this
for example this is the memory context
so and by using the long-term memory we
have extracted that I have already told
her that my favorite movie is X minina
also somehow Pizza is semantic
semantically similar to movies also I
don't have that many um so that many
records in the longterm memory but yeah
this is all we'll be explained in the
next lesson so really subscribe if you
haven't because I think it's going to be
a really good one but yeah it not only
allows you to run the graph it also
allows you to debug it or to inspect it
right we can see for example what was
the result of the context injection
right we have for example got that the
current activity is that an evening
routine while catching up on NASA's
latest exoplanet discoveries right so
this is AAS activities right and then we
can see how the router the output of the
router was conversation right so that
was what we so for the response type is
conversation and yeah this is truly
truly powerful you can even rerun uh
from different parts of the of the graph
you can even change the state or
understand the state rerun it from that
part and then you see right so you can
change something about the about the
memory context just something about the
state and rerun it from that point so
extremely extremely powerful for you to
debug your applications and how do you
set this up you might ask so it is quite
How to set up LangGraph Studio?
simple so they have this article that
explains you very very simple so you
have two ways so you can you could use
the langra desktop app that for me was
causing a lot of error so I actually
went and used the development server and
the only thing that you have to do is to
pep install um this package or in my
case via UV so UV pep install this
package and then just launching it with
lra so if we open cursor we see here
that I just run this so by just running
that it
directly opens up langra Studio oh and
something else that you got to have is
just in your project directory you got
to have two things so one you got to
have your uh graph already compiled and
you got to have this in a in a
independent variable so that you can
then take it using the Lang graph. Json
so you need this file and in this file
you have to set up the dependencies so
this would be all the dependencies so
this will take the um the PIP project to
with all the dependencies and then you
have to point at the agent or the agent
so you might have even more than one
agent so here we point at it right and
you also use your M file so that it
takes all your environment variables for
example your Gro API key to be able to
Wanna know more?
run inference using Lama 3.3 and that
concluded lesson two of ABA the WhatsApp
agent and I really hope you got a base
understanding of how langra works but if
you did please write me a comment in the
comment section below with just anything
that wasn't clear or just any questions
that you might have and if you go to
this part of the video I would actually
appreciate if you can just tell me a
little bit about yourself so about how
much experience do you have with python
with programming with artificial
intelligence so that I know more or less
who is watching these videos and and
then I just tailor the next lessons to
you also I'm going to put like always
links to all the relevant information
and something that I think is really
amazing is just lra Academy has a free
course on langra that is really really
good I I did it myself and I actually
recommend it and finally I want you to
Real-World Applications
to understand that what you have learned
today with langra and these kind of
ageny Frameworks allows you to build
very very powerful real world
application so um AA so far is just kind
of like a sophisticated um
conversational machine right she's able
let's say to pass the tting test she
really acts humanly but maybe this
doesn't have those real war implications
so you can really think and build um
those applications right so think about
for example um an automated appoint
appointment setting right so you via
WhatsApp you can set confirm and
reschedule just dates that you have in
your business or um or business that you
maybe you want to sell this service to
maybe like a personal assistance or
maybe like in the movie here you can
have a system like Samantha that manages
your calendar the emails tells you about
the weather and everything could be
conversational in WhatsApp more things
you could even have maybe like a
customer support agent that is connected
via a database tool to your database and
then it tracks the orders and maybe
manages returns and more and more so
think about a financial advisor so there
are different API keys so apis that
connect to maybe like the Yahoo finance
API that connects to the market I you
can get Market updates also you could
use x AI AP ke so you can get real um
real time information about what is
happening in Twitter or in X and then
maybe this can tell you about the market
and think about Healthcare as well so
you can have um a conversational
WhatsApp agent that maybe sends
reminders to to patients or maybe like
in case of urgency it acts right it does
something and you can build these
applications by just writing the
specific tools for this kind of use
cases and just give that to the agent
and that's it it's just notes edges and
estate and we have learned that today
well that that really was all for lesson
two I'll see you in the next lesson
byebye

### WhatsApp AI Agent Tutorial 3: Unlocking Ava's Memories | Intro to RAG & Vector DBs

Intro
hello everybody and welcome to lesson
three of Ava the WhatsApp agent in this
lesson we're going to cover a couple of
things that I have already here written
so first of all we going to check we're
going to understand how Ava uses her
memory both the shortterm and the
long-term memory then I'm going to
introduce you to the concept of rag I
think one of the most important Concepts
in gen applications and it's I think
it's used in most applications in one
way or another um as part of this rack
we are going to explain you what is a
vector database and I'm going to explain
you all the different database providers
so the vector database providers that
there are and why we chose to work with
quadrant then we are going to dig deep
into the code and actually we're going
to understand how the shortterm memory
is implemented using my SQL SQL and also
how the long-term memory is implemented
using quadrant and finally I'm going to
show you how you can set up your own
instance of quadrant Cloud because
actually they have a free tier that
allows you to create your own um free
cluster using Google Cloud okay so suing
Short-term Memory
in we have the first diagram that Miguel
has prepared and as always it's looking
beautiful this is a really cool diagram
because it shows both the shortterm and
the longterm memory in the same kind of
like picture and I think you will
understand it very very very well so
let's start by looking at the shortterm
memory that we have represented here on
the left for storing this shortterm
memory we are using S and is and
everything is running directly in the in
the docker instance or in the local
machine and what this shortterm memory
stores is actually the graph state that
we already reviewed in the previous
lesson so if you haven't looked that
video you should go and look for lesson
two but what we have is a set of
parameters that we have selected for our
application and those are the summary of
the conversation until that point the
workflow that has been selected by the
router either conversation an image or
an audio the audio Buffet itself the
image path itself as well the current
activity that Ava might be doing and the
memory context which refers to those
memories that we retrieve from the
long-term database plus of course course
all those recent messages of the
conversation that you're having right
now with ABA a conversation that I want
to review with you because I think it
reflects very very well how we extract
those relevant memories and let me come
back quickly to the diagram of the
previous lesson so this H the graph
diagram right in which we represented
those nodes and edges that conform our
brain or our graph or ABA brain and as
you can see here the first note that we
have is just the memory extraction right
so so just remember that and let's come
back to the memory diagram but
everything will be super super clear
once in a couple of minutes we review
the code okay back to the memory diagram
Long-term Memory
and now let's pay attention to the right
side part of this diagram so the
long-term memory that we Implement with
quadrant and by looking at this we're
going to start already understanding how
we extract those relevant memories so
let's start from the top right so we
have AA just saying hello I'm AA and now
Miguel will be saying hey I'm Miguel
nice to meet you so what it starts
Happening Here is that AA or or the
system that we have built or aa's brain
will process each of the messages that
Miguel sends or that the user sends
understand if there is something
relevant so something that is special to
this user right something that for
example denotes a name or where is he
from or what is his profession or what
does he like to do um or what is he
doing right now in the moment so so this
will probably remind you of how chat GPT
mes remembers the conversations that you
have had with it and right like probably
in in chat you have seen that when you
tell something important to to chpt for
example so for example I'm building this
cool machine learning or artificial
intelligence project called AA blah blah
blah blah and now probably you will see
or I will see my messages something like
memory updated and what it what chbt is
doing is more L what we're seeing here
so let's look at at what we have here so
AA you will maybe like just have a
normal conversation with you and maybe
like she will she will ask you hey where
you from and Miguel will say I'm Spanish
so this means that AA will understand
okay Spanish this is relevant I'm Gonna
Save this in my long-term memory same
thing right like the profession so ma
engineer um so you would have a a kind
of like completely normal conversation
with AA but in the background ABA will
be saving those key aspects about
yourself and what Miguel has put in in
this diagram nicely with the string or
or or that piece of text that ABA will
get from the message and and then also
this array of points or circles so those
would be so those would represent H the
embedding Vector which are actually the
elements that are saved in a vector
database and I'm going to explain you
this now in the next diagram all right
so we have already seen how we extract
RAG Explanation
memories from the recent conversation so
more or less we have understand how it's
done but we still don't know very well
what is an embedding vector or an
embedding and now I'm going to explain
you how we inject relevant memories and
we actually do this thing by using this
framework or this concept called
retrieval augmented generation and by
explaining you this along the way I'm
going to explain you and you're going to
understand super super well what is an
embedding what is an embedding model
what is semantic search and what is a
vector database so let's get it started
so retrieval augmented generation is a
three-word concept and as a three-word
concept I want you to understand it as a
three-step process so first of all
retrieve second augment and third
Retrieve
generate and let's start now by of
course number one retrieve so what
happens when Ava um gives you an answer
is injecting some relevant memories
before giving you the answer right so
those memories will be injected let's
say in the prompt so those memories that
we retrieve are the result of doing
something called semantic search and now
let's let's go a step by step to
Semantic Search and other terms
understand how we do the semantic search
and what it actually represents what it
actually means so first of all we have
just um a query or a question or just a
sentence that is just a string right
it's just it's just plain text so what
we do is we use an embedding model to
generate an embedding or an embedding
Vector which is simply a vector
representation of an object text image
video or audio and by Vector
representation we just we just say
numerical representation right as we
have it here it could be something like
0.5 .4 0.8 0.1 in usually of course in a
higher dimensionality than just four but
essentially it's just that right it's
just a vector so a numerical Vector so
what is an embedding model then so an
embedding model is a model that converts
those objects into meaningful Vector
representations and and here let's pay
attention to to meaningful and by
meaningful let's understand it from the
text perspective so it has a semantic
meaning right and this concept of
semantic meaning H ties very well with
the next thing which is semantic search
so semantic
search is just doing kind of like
nearest neighbors for Vector
representations a nearest neighbor if
you don't know is a technique to find
those close elements in regards to a
distance and finally last thing from
this list what is a vector database then
so a vector database is a is also called
like a vector search engine and that
what it does is it manages so it helps
you indexing retrieving and quing these
embedding vectors and since I know this
Vector DB – Zooming In
might still not be completely clear
let's zoom in in what a vector database
is so a vector database would have store
these high dimensional vectors but now
for the sake of this explanation let's
just imagine that we have just two
dimensions and what I have here
represented in green are those relevant
memories that we have already extracted
in past conversations with the user and
in blue we have that query H for which
we are doing the semantic search so what
we are actually doing is finding in this
High dimensional space so here in this
simplified version in this
two-dimensional space those vectors that
are the closest to the query so here the
query was um that I would that I could
be asking AA right so I could be saying
hey remember my favorite movie and ABA
before giving an answer it will look
into her long-term memory into her into
the vector database and it would
retrieve those relevant memories so what
are so what could be those those that
have a similar semantic meaning so let's
just look at this sentence right we have
remember my favorite movie so what are
the things here that have semantic
weight so that would be for example
remembering favorite or movie right so
here we can see on on movie movie and
film are semantically Clos because those
represent the same thing and similarly
um as well here movie and movie of
course that's that's even clear and
those things are and so these factors
are very close by because they are
talking as itially about the same thing
movies so this way you could imagine
also different clusters or different um
arations forming by different topics so
another topic could be something about
food so we have here that ABA has stored
in her memory that um the user loves
pizza and also he likes to eat healthy
could be contradicting but but yeah
those things are about eating right so
they are close by in in the vector space
same thing he's from lanero he lives in
Madrid so this things could be related
to um related to to a space or to cities
and those things are more so these
things these two things have more things
in common than pizza and lerot so this
more less would be the whole idea of
semantic search I hope you understood it
and if you didn't understand it please
drop me a comment below and I'll and
I'll try to explain it myself so I'll
try to give you more examples and maybe
I can even just send you a couple of
articles that explain this as well so
Augment & Generate
with that we have the First Column of
the first part the retrieve part which
is actually the only complicated part
because the augment and generate parts
are very simple you'll see so by augment
what we mean is just that once we have
retrieved this memory so the closest one
was his favorite movie is X minina we
are going to inject that in the prompt
uh along with the current conversation
and those system instructions that AA or
or the agent is following and finally
once we have this complete prompt what
we do is just to invoke a large language
model in our case in the case of Ava we
are using Lama 3.3 um via Gro and we
just invoke this model to generate an
answer and the answer could be something
like xina right so this shows how we use
H this framework rag rment generation to
inject the relevant memories into aba's
brain so let's review that again right
so we take a query like remember my
favorite movie we use an embedding model
to generate an embedding and then we use
a technique called semantic search to
look in the vector database for those
embeddings that are similar semantically
we extract those or we retrieve those in
this case could be something like his
may his favorite movie is X minina then
we aent right we inject this into the
prompt and then we use now so now with
all this information we call a l model
to give you an answer which is something
like X minina right awesome so this
would more or less represent a retrieval
augmented generation right but there are
other Advanced things that I want to
Chunking
just quickly mention right which is this
thing or this world con called chuning
that you might have heard before and the
whole idea of chuning is that you so in
this case in the in the case of memories
we usually have short um sentences or or
short messages but what happens when you
want to create a vector database based
on books for example or long pieces of
text so the whole idea is that you have
to divide um divide or chunk those long
text into shorter chunks so that would
Choosing Embedding Model
be chunking and also an invading model
right so um in the same way that we have
a a model for Generation we also have a
model for embedding and here um you
should select an embedding model
depending on more um depending on that
meaningful representation that want that
you want to get from the data right so
um an example could be for example if
you are talking in in a very specific
language right if you're talking in
English then it's simple but maybe in
Spanish there are models that work
better than others so you would maybe
use an embedding model that is better
for only Spanish or for a multi-lingual
application so that could be an example
another example could be if you are um
building a rag for a very specific um
for a very specific domain for example
biology or chemistry right so where you
have all these technical words and maybe
if you use a generic embeding model
those would be diluted so you want a
model that is able to find that
meaningful representation between those
um sentences and and terms and if you
want a more detailed video about this
Advanced Techniques and and just rag in
general just let me know in the comments
Vector Database Providers
and I'll and I'll make it and now a very
quick overview of vector datab base
provider so as in the past lesson there
are many to choose from so in the past
lesson it was a IC Frameworks now we
have Vector databases right so there are
plenty I think I listed more or less the
the ones that I know but I believe there
are a couple more and again as with the
identic Frameworks you shouldn't be
using them all just choose the one that
you like and just go for it because they
all perform very similarly because they
are all kind of like competing among
themselves the things that you want to
maybe be paying attention would be like
the speed of the semantic search of this
retrieval but I think more or less they
are all equally equally fast um but I'm
Why Qdrant?
going to tell you why we chose quadrant
over the other ones um I myself have
used uh chroma in in a lot of projects
but yeah for this project we use quadran
for H three reasons so the first reason
that is actually quite quite important
for me is just that it's open source and
I like when projects are open source
quadrant it is H secondly you can
selfhosted so that means that you don't
actually need to pay for it so you can
um have a so you can integrate that in
your in your own server in your cluster
in whatever in whatever you want and
they have also a nice docket image for
you to do it simply and finally because
of their a free tier in the cloud option
so they have a a cloudbased um option to
use quadrant and they have a free tier
um powered by Google Cloud which is very
very convenient so you just need to um
get an API key and just install a a pep
library and and everything works and
that's that's really a nice user
experience or a nice developer
experience and at the end of this video
I'm going to show you how you can get
thata and how the quadrant cloud
looks like which is very very simple
Code Overview
okay and let's now have a quick look at
the code and I think by by really
analyzing a couple of things that we
have here written everything will make a
lot of sense and and I promise you it is
quite simple so um as for the shortterm
memory I don't know if you remember in
the first um in the first diagram that
we saw in this lesson we had on the left
side hand the memory right and we and I
told you that we had that what we do is
just essentially just writing down the
the graph State um in in local this
let's say by using um and the the graph
state was this set of parameters the
summary the workflow the AIO buffer so
this is represented by the class AI
companion state that that you have in
the code which by the way just remember
that you can access this code by looking
at the report that I have linked Below
in the description everything is
completely open open source and you can
have access to the entire uh application
right now so in order to persist this
graph state in memory which contains all
those recent me messages and so on what
we use is this um async SQ L saver and
we use this as a as a shortterm memory
right and just essentially as I said we
um are this right now um locally right
you could store this in a in a in a
postgress SQL or whatever but just for
the sake of this project we have decided
to store it in memory and yeah
essentially we just have this ex
database leaving here and by using this
we can recover those conversations or
those recent messages or those or that
graph state so what you have to do then
is just use this checkpoint H parameter
when you compile the graph
and you give that a shortterm memory and
that would be all quite simple as I said
and now for the longterm
memory remember remember that graph
diagram in which we had the brain we had
those two nodes we had the memory
extraction node in which we extract
those relevant pieces of information
from the conversation and also the
memory injection node which what it does
essentially is this uh retrieval
augmented generation framework so let's
look first at the memory extraction Noe
what we do is we just get this object
that we have created called memory
manager and we what we do is just
extract and store those memories and we
just pass that last message and if you
look at the code you will see the it
better but let me just jump into the
most important thing which is maybe the
prompt right so we have this method
analyze memory in which we um create a
prompt and then we invoke a message on
that prompt and what we want to do is
that the output of this invocation
should be kind of like a memory anal is
you're saying is this message important
and how um and how the message should be
formatted to be stored right and this
goes along with the prompt and the
prompt essentially does what I told you
in the very beginning of this video
which is to instruct the model on doing
what I told you in the beginning which
is um more or less what what what chpt
does which is to understand in there are
if there are important facts mentioned
in the message things about personal
personal details so the name the
profession what are the preferences life
circumstances so those things that are
important will be saved as a memory so
things that are that are important for
example would be something like a
message like how are you how are you
doesn't doesn't convey or doesn't has
doesn't have any relevant information so
that would be discarded by this kind of
prompt and then what we have is the
memory injection node that what it does
is the retrieval of those memories and
then the injection right so we are still
not doing here the generation but we are
um using the memory manager to get those
relevant Memories by using the vector
database and then we are um returning
this um as the graph right so this is
kind of like the augmenting because now
we have this context and it is then at
the final stage when we use the
conversation node to generate an answer
that the memory context is used and we
can quickly review H that prompt which
is this one H in which you can see how
as part of the the whole system
instructions and so on we give um this
right we give the memory context as the
user background so here is where we will
put all those H memories that are
relevant to answer that specific query
and for retrieving we have this method
get relevant memories which uses the
vector store or vector database to
search for those memories and the search
searching itself is just using a
quadrant client to search over a
collection and a collection is just as a
table let's say in in in SQL so this
would be more or less where you collect
your your different embeddings and it's
of course this search method the one
that does this semantic search using the
query embedding right the embeding of
the query so we have to use an embedding
model to encode that query and once we
have that we also say how many K right
so remember like this nearest nearest
neighbor so how many um how many of
those closed um closed vectors we want
to retrieve and for this whole thing to
work using quadrant Cloud the only thing
that you have to do is just use the
quadrant client which is um again it
comes as a python library and you just
need to give um the quadrant URL and the
quad API key that I'm going to show you
right now how you can get it so here we
Qdrant Cloud Overview
have quadrant Cloud when you are going
to be able to see all your clusters and
as I said in the beginning you have a
free cluster powered by a Google cloud
and yeah you simply you can just create
it by just clicking create here right
now I cannot create it because I have
already one but once you create it you
just give it a name and once you have
that name you're going to be able to
access the database by opening the
dashboard here and this is going to show
you all the collections that you have so
for example we have the The Collection
longterm memory of course for for this
project and we have H different things
right for for example I have things that
ABA has gotten from my conversation so
his s the Canary Islands but lives in
Madrid well she well in this case it
would be he but the whole idea of my
message maybe my conversation with ABA
was that I like to do CrossFit so ABA
got okay he enjoys CrossFit because this
it's something important maybe she will
remember um a couple messages later when
I when we talk about sports and here as
well another thing you can see is just
all the other Meta Meta data that you
have along this Vector would be for
example the time stamp or the length of
the vector itself and uh finally um as I
said you just need to set this up by
just getting an API key and just setting
the URL and that's it right so you
create an API Key by just clicking here
create I already have one and then you
also uh use the endpoint or the quadrant
URL and that's it you set that up as an
environment variable and you are all set
Outro
so that concluded lesson three and I
hope you enjoy the video and if you did
just please give it a like and also
subscribe to my YouTube channel and hit
them and hit the notification Bell if
you want to be notified when we upload
the next lesson which should be next
week bye-bye

### WhatsApp AI Agent Tutorial 4: Giving Ava a Voice | Whisper & ElevenLabs

Intro
hello everybody and welcome to Lesson
Four of Ava the WhatsApp agent and as
you could probably guess by the title of
this video this lesson is going to be
all about voice both in regards to how
we process the voice that we send via
voice notes to AA and then how she can
answer back to us with another voice
note so for that we're going to start by
reviewing this nice diagram that Miguel
has prepared that is going to be all
about the voice flow then I'm going to
tell you briefly about both um stt
models which are a speech to text models
so those would be the input models and
TTS models or text to speech models
which would take care of the output
audio after that we're going to review
the code we have prepared two different
modules one for TTS and the other one
for SST and the code is quite quite easy
to understand and to follow so we'll
have a look into that and finally I'm
going to give you an overview of the 11
Labs platform or the web app that is
quite amazing actually because it allows
you to creat synthetic voices just for
from a prompt or it also allows you to
clone your own voice by just giving a
couple of seconds of your own audio of
your own recording and many more things
like voice changing or generating sound
effects so what happens then when we
Voice Diagram
send an audio via WhatsApp to Ava so
what happens in the background is that
we are obtaining this WhatsApp file from
WhatsApp Cloud we get that into our
local machine and we use whisper to
transcribe the audio and we use whisper
via Gro I'm going to explain you um a
little bit about why we use Gro and why
we use whisper as a model then once we
have the transcription where we have the
text message we process it via our brain
via our L graph graph and we process it
just essentially as you would as we
would process also just a plain message
that you would write in WhatsApp so to
get the response we use the Lama 3.3
model via Gro which is something we
already covered in lesson two so if you
didn't see that lesson so you should
watch that one and after that we're
enriching the context of the message by
just checking the long-term memory and
the shortterm memory for that as well
check the previous lesson on on memory
but yeah essentially after that what we
do is we once we get the response where
we get that text message what we do is
we do the TTS so we convert that text to
a speech and we do that by using the 11
flash H 2.5 model from 11 Labs which is
actually especially designed for kind of
like conversational applications because
it's quite quite fast and still H the
quality is really good and finally once
we have that audio what we do is we
upload that to Whatsapp Cloud so that
then it appears in WhatsApp so in short
STT and TTS
if we simplify that diagram even more
what we have is this so we have firstly
the part in which we do a speech to text
also called automatic speech recognition
and we do this by using the model
whisper then after that so once we have
um computed the text what we do is text
generation as always and for that we use
the model Lama 3.3 and then finally once
we have that generated text or that um
response text what we do is TTS which is
text to a speech and for that we use 11
Labs so why these two models so why
whisper for for SST and why 11 labs for
for TTS so in short I will tell you is
because they are the best but instead of
just telling you what I'm going to do
today in this video is going to I'm
going to show you a different resources
that I use to decide or to select the
best model for each task and I usually
Leaderboards
do that by just checking different
leaderboards so the one that I have here
which is from artificial analysis I
think it's just the very best one
because it has these very comprehensive
um diagrams in which they show um the
accuracy against the price and and
different and different other metrics
and here at a glans H you can see which
are the models that have um the lowest
error rate and also the speed Factor so
speed is of course very important and if
we look at the diagram over here what we
see is just many many different mentions
to the model whisper so why wiper is a
model gener so created by openi but they
open source it I think it's one of the
very few things that op has open source
and that allows for different companies
to build Solutions on top of it so um
the one that um that we're currently
using in this project is Gro because
they offer a free API key and is one of
the best ones but right now they are so
many different um inference providers
are competing just to get whisper as
fast as possible and right now for
example it seems like the fastest one is
via fireworks but still Gro is very very
fast as you can see at 200 um input
audio seconds per second which is crazy
so this is one way for me to usually
just check Which models to use for each
task another one that I really like is
to have a look at hagging face
leaderboards here we have the open AI
whisper latch model that we are using
right now and you have different other
models so it seems like in this um
leaderboard the Canady 1B model from
Nvidia is the very best to be honest I
never never use it because I think whis
the whisper model is the standard and
the ISE of use via this inference
providers issu
great then as for text to speech we have
of course a laps here being one of the
best ones so it seems like by by this
standards the open AI text speech is the
very best in quality but we were
actually went for 11 laps not only
because of how good it is which is in in
my opinion so to my ears the best
sounding one in terms of like how
natural and humanlike um the voices
sound but also because of their
developer experience so just how easy it
is just to get the API key and just get
your your text generated into into
voices and also all the features that
they offer for example um cloning your
own voice or creating a synthetic voice
only from a prompt and I'll show you all
that in a couple of minutes at the end
of this video and if we look at these
other graphs we can also see that levs
is still quite fast you're generating
365 characters per second of generation
time but in terms of price is definitely
not the best but as I said I think due
to all the features that they provide I
think the price is still quite good and
if you don't want to spend a cent you
have also the option of using open
source models so here for example we
have the kokoro model that I was
released I think a couple of weeks ago
and as as in this rank it appears it's
just one of the best I've heard it and
I've heard how it sounds and it sounds
really really good but again just the
ease of use of a level UPS I think in my
opinion wins at this point and you can
find the links to all of these
leaderboards and all these websites in
the video description below and also if
you want to read about this thing and
just learn even more I'm going to leave
as well the link to Miguel's newsletter
in the description so you can just
follow everything that we have seen in
this lesson but Al but in but in his
Code Overview
article and now let me quickly give you
an overview of the code which is
honestly super simple so we have two
different mods so we have the text to
speech module and the speech to text
modules both under the speech directory
in and since both these services use API
keys to actually do the hard work the
code itself ises very little so what we
do in the case of the text to speech is
we use H the level ABS library that you
can just install it and import it and
then just simply use that client know
that the client that you instantiate via
the library and just just generate you
just give the text
you select the specific voice that you
want this audio to have so in our case
we created a synthetic voice of how ABA
we think it should sound and and we use
that Voice via the um voice ID and that
would be all actually then we just
generate the vites object um from this
generator and we send that to the
WhatsApp Handler which is something that
we will see in lesson six so everything
about WhatsApp and how everything works
with WhatsApp Cloud we be explaining
that lesson and then for a speech to
text what we do is use something similar
so in this case we use the gro library
and we again instantiate um a client
object so once we have this client what
we do it's just something very very
similar so we use use one function that
Thea which is the transcriptions create
and what we do in this case is just the
contrary right what we do is we send an
audio file we specify which model we
want to use of course is going to be the
whisper latge model as we said before
and we also tell the language that we
using so that this could help I think um
it is actually not mandatory to to give
the the the language and the result of
this call is just the transcription so
the the text and so that would be all so
you would just return that and the
execution will just continue by just
generating the the the message from this
text right and finally I want to give
ElevenLabs Overview
you a quick overview over 11 Labs the 11
laps platform so well this is just the
the landing page or the main page I
think here you can already test out the
text to speech so maybe we can just do
that already so we can just click
play and we should the 11 Labs voice
generator can deliver high quality
humanlike speech in 32 languages exactly
so um so we already got that and and
actually the the the quality of the
voice was was incredible was really good
um and here you can just select the
different different voices for example
Charlotte or Brian so this this would be
voices that are already generated by
them the 11 Labs voice generator can
deliver high quality exactly right but
let's just go to the app so I can just
show you a couple cool features so I
think the features that we are mostly
interested in for the purpose of of this
H demo and this project Ava I think it's
the Tex of speech that we saw before so
here we not only have the option of
going and using those um Library voices
you can also create or use your own
voices so for example we have AA here
which is the the voice that we using in
the project and we have the model so we
have the multilingual model which is
kind of like the the the best model so
the highest quality and also the flash
model which is cheaper and and also just
it's faster so this is the one that we
use in in WhatsApp in the app but maybe
just for now we can just um click on on
MultiLing just select this one and we
can use um yeah for example this is just
one message that abat told me a couple
of days or weeks ago in WhatsApp so we
can just generate speech Alex Garland
yeah he's a genius X mackina and
Annihilation both mindblowing films
exactly so that's that's amazing right
so the that was generated was actually
respecting all those commas and and
exclamation so really really good so
here as well in this page you would have
the option to for example change the
speed the stability or the similarity
but I think right now it's just as
default and it works quite well and then
the other thing that I wanted to show
you is actually how to create these
voices so you have these voices here um
that we just can use click and then
these are the different ways for you to
create a voice so we for example created
Ava by designing a voice so this allows
to to just write a prompt for example
this is the one that comes by default
now that that we're testing and then you
just
generate a voice and and you use this
text to to prev the voice and just let's
just hear um what it sounds the night
air carried Whispers of betrayal thick
as London Fog I okay the night carried
Whispers of betrayal I like this F I
adjusted my cuff links the night air
carried Whispers of betrayal thick as
London and this one I think is really
good I think this one was was the best
one so what you get is just three
different voices of kind of like in M
Journey that you that you get four
images or something or three images here
you get three different voices so you
could select that voice give it a name
and just continue to use in it and the
other super cool feature that I wanted
to show you was the the actual um
instant voice clone so that you you can
just record an audio of yourself so it
would generate so it would clone your
own voice so we can just h test this out
so only 10 seconds of audio are required
let me just read this for example so
avoid noisy environments check
microphone quality use consistent
equipment okay you just read a couple of
things and and and it seems like I
already have already 21 seconds of audio
and this is already ready so I think if
I continue to record more audio that
would increase the quality but let's
just try and see what happens
now so we just need to fill a couple
things so we can just put my name and
then I was talking in English and the
description is just me my
clone and I can just accept
that and let's try out my voice let's
just try to
generate an audio with the voice Jesus
so let's just try the same
prompt Alex Garland yeah he's a genius X
MAA and Annihilation both mind-blowing
films okay that didn't really feel like
me maybe it's just because the speed is
a bit too high H I think it was at one I
don't know we can just maybe try to
increase or change a couple of things
similarity High let's try to regenerate
that one Alex Garland yeah he's a genius
X macina and Annihilation both
mind-blowing
films okay okay I I don't think I sound
quite like that but but I I can see the
resemblance but yeah do consider this
was just the the voice that was clone by
just giving 20 seconds of my of my own
recording so probably if I just give a
couple of moment minutes the quality
would be better so yeah really cool and
if you want to try a level UPS yourself
I'm going to leave a a link below in the
description so that you can just H
directly and that was all for Lesson
Four so I hope you enjoy the video I
hope that you learn a couple of things
and just let me know in the comments as
always as always if you have any doubts
or if you want if you want me to kind of
like dig deeper into something that
wasn't clear in this video and of course
if you like the video I would appreciate
a lot if you can just give it a like and
And subscribe to my YouTube channel and
bye-bye and and see you in the next
lesson

### WhatsApp AI Agent Tutorial 5: Ava Learns to See | VLM (Llama 3.2 Vision) and text-to-image (FLUX)

Intro
hello and welcome to lesson five of Ava
the WhatsApp agent in today's video
we're going to review a couple of things
and everything is related to vision and
how ABA can see the images that you send
and also how she can create or generate
or send photos of her own activities so
for that we're going to do a couple of
things so first of all we're going to
have a look at um Miguel's diagram in
which we can see just everything that
relates to the image flow let's call it
then we're going to be looking at this
diagram that I created in which I I will
try to explain to you and I think I and
I think you will understand what is a
vision language model and also we're
going to answer the question if um are
Vision language models the same as
multimodal large language models and and
finally I'm going to do a a small review
of all the text to image models well and
like always I'm going to give you a code
overview of the the important the
important pieces of the code related to
everything that I'm going to explain you
here and also I'm going to give you a
small um overview of togethers AI
inference platform which actually
provides a free endpoint to use the flax
chel model that actually Ava uses to
generates the images Okay so let's start
Image Diagram
by reviewing Miguel's diagram that again
explains super super nicely everything
that is happening in the background so
everything that relates to how images
are treated so first of all what we have
here is just what you would do if you
send an image to Ava right so you could
you could say something like hey look at
this picture so this is Miguel's golfing
and you would set you would send an
image with along with a text right so
what is happening in the background is
that we are using Lama 3.2 Vision model
and I'm going to explain you everything
well I'm going to explain you a little
bit about that later and we use that via
Gro again our usual inference provider
that is just super super fast and by
doing this or by using this Vision model
where we create or what we get is a text
description of this image so then what
we do is along with this text
VLM Explanation
description we also send the the message
that the user so in this case Miguel is
is giving right so for example out golf
in this morning what about you and that
would be treated just as as text right
and then we could use directly our Lama
3 3 um 7 video model just to generate
the answer um about what AA is doing but
what we have here is an explanation of
what would happen if AA decides with her
brain right with this router that we
explain in the previous lesson so what
happens is now ABA decides to answer
back to you with another image or with
an image of what she is doing at the
moment so what would happen in the
background is that we first we would get
a um aa's current activity so for
example this could be um at 9:00 a.m. so
9: to 10 a.m. could be something like
okay AA is programming because she's
also a machine learning engineer so
taking this um activity we would use a
prompt so we use another llm call to
generate an N scenario so the scenario
would be a rich description of this
activity and then this is actually just
the the the text that goes into a text
to image model I'm going to explain you
a little bit about about that later and
but that model so this model that we use
as mentioned before this is the flaxel
model which as I said takes this text
and generates an image and we run this
model via together AI inference provider
um which again offers this free endpoint
which is amazing just to for for
building this kind of these kind of
applications right and finally along
with this image that ABA would send to
you via WhatsApp she would also send you
um a text message and that text message
also um involves just having a look at
the memory as we explained in the
previous lesson and just again running
the model Lama 3.37 billion and that
text could be something like building an
LM from scratch while the b in ramen
right and this would be accompanying the
image or the scenario image that ABA has
has created or has imagined and now how
can Ava see or understand the images
that you sent to us or how can she
create that description from an image so
so that's possible right now because
nowadays there are a type of model that
is called a vision language model and I
want to I I want to explain you um just
briefly how they work and I'm also going
to refer to you to a really nice article
that explains this even better and and
much more in depth but essentially what
we have is a model that not only takes
text as an input right it also takes an
image so what this model does internally
is that before we actually do the whole
kind of like processing and and just
getting a text back what we do or what
this model what this model does is it
has an encoder so so all images go
through this encoder that just encodes
right that it generates Vector
representations or embeddings and again
we we saw the definition of an embedding
in the previous lesson so in this case
is an image embedding right so this
vector or numerical Vector
representation from an image and in a
similar fashion it also takes the text
embedding it tokenizes right so it
divides the text into different tokens
and it embeds those um tokens into text
embeddings right and now now that we
have both image and text eddings in
different ways or in different yeah in
different forms we combine those and
produce a text output and to explain you
this just a l better let me just use
this fantastic article from Sebastian
rashka that explains it even better so
um we have different methods for let's
say Fusion or combining these embeddings
so the text embeddings and the image
embeddings so one approach one method
would be just this unified embedding
decoded architecture and what is
happening here is that we concatenate so
we we get this um so from an image we
apply this image encoder we get this
image patch embeddings and we
concatenate those with the text um token
embeddings right so we apply a tokenizer
an embedding layer and then all these
together goes through the model and then
we generate the the output text so that
would be one method
and the other method I think is just a
bit below I
remember yes yeah and the other the
other method would be something that is
called cross modality attention
architecture in which this Fusion of of
the embeddings happens at a later stage
and so we do take again both the text
embeddings and the image embeddings but
now the text embeddings the text
embeddings goes first into the model so
into these backbone or the yell M
backbone like like a GPT model and then
it is in the middle of this processing
we would take the image embeddings and
we would put this in this mask
multi-head attention and this works via
this cross attention mechanism that I
really really recommend you to read this
article because it is very well
explained in even though it's it's quite
a complex concept and coming back now to
the diagram so I have this question here
MLLMs vs VLMs
so is a Vis language model just the same
as a multimodal large language model
that you probably have heard many many
times recently so this this whole um
world so the reality is that they are
quite similar but they are not the same
so um a visual language models are
actually a subset of multimodal large
language models so so why in this case
so actually because of two different
aspects so second so one one would be
the output so the output modality
doesn't need to be just text it could
also be an image or audio and same thing
with the input right so a vision
language model only takes images or text
but a multimodal large language model
can also take and audio or even video
and you actually have many examples of
MLLMs Review
multimodal large language models so
probably the one that you that you use
the most is gbt fr or Claud or or Gemini
H but I think I want to just throw you
to this chart that I created so um
something very interesting that is
happening right now in in the field of
AI just all these ADV advancements that
are happening not only in regards to
these big expensive models but also like
in these smaller opensource models and
there are a lot of Advance advancments
happening happening as well in regards
to visual so Vision language models so
multi multimodel model so one that came
um a couple days ago it is Fe four so
the fourth version of of this small
model from Microsoft and now it has
multimodal capabilities and in
benchmarks it looks really really well
so it's kind of like competing with
Gemini and and all these bigger more
expensive models also qu from Alibaba I
think
is amazing as well and the one that we
using in this project is Lama 3.2 and
all these models are even open source
right so what this really represents or
what this really means is that the the
smaller the so the the the smaller in
size the models are this means that
maybe they're going to be able to run or
soon they're going to be able to run on
um your mobile phone or your directly on
your laptop so that is going to be just
so much better for for us users and also
with the smaller size it also comes a
smaller H cost so uh this also is just
so much better for us uh to build um
multimodal agents so for example um an
agent like operator that is able to um
take a screenshots of everything that is
happening in the in the browser and take
actions like clicking H clicking or or
writing text and then just do tasks like
buy me this book in Amazon or buy me a
flight to larot next week so these kind
of models are going to be powered by by
this smaller H Vision or multimodal
large language models and now quickly
Text-to-Image Review
before we jump into the code I want to
just give you a brief overview of what
is a text to image model and and just
the different h options that that you
have so um an image so a text to image
model is essentially is just a model
that is able to take text as an input
and output an image so it usually does
this via this um this thing called
diffusion that I'm not going to explain
in today's video but I'm going to tell
you just the different models that are
available right now um and briefly why
we are using fla yeah so um fla is a
model that came out recently last year
is from um um a research laboratory from
Germany and they actually released the
the weights of the model so that there
are many inference providers that have
created end points for you to easily use
this model via an API right so you can
integrate this in code and this is
contrary to what was happening before
which is that you would only be able to
access this high quality um text to
image models via VIA a user interface
right so the the biggest example here is
M Journey which is a really good model
or at least it used to be and I think
now um these other Alternatives so I
have here FL
IM imag imagine 3 that came out super
recently so I don't know if it was a
couple of weeks ago or months ago is
incredible so probably the best to my
eyes and it also provides an API key so
an API um an AP so an access to it via
VIA API and also there are other two
which are Rec recraft and edram that are
again incredible in quality I think they
they look very very real and like in the
previous video I I want you to to have a
look at this um artificial analysis
website where there are um a leaderboard
or a comparison between all these models
and you can see here that by this
leaderboard the recraft B3 model is the
best but is onire so it's very very
similar to a flax 1.1 Pro and and and
now you can see that there are different
flax mentions here so you have the pro
version which is like kind of like the
bigger model you also have Dev which is
also like quite big and then you also
have theel model which is German for
fast and and this model is just smaller
faster and and this is the the nice
thing about this thing is that since the
model since the weights are open and
every company just can take it um all
these companies are competing to to to
to use use their Pro so their platform
and this also is is a benefit for us
Together.ai Overview
user because there is this platform
called together AI that offers the flax
model for free so you can just go onto
their playgrounds right so into this
user interface and just do something
like just write a right so it could be
something like um run so dog running at
a park and then enter and super quickly
you're going to have an image I mean
look at this it just looks amazing and
you can just run it again and and this
is free H so this is beautiful so here I
think we can see more than four legs
which is something that can happen with
these models especially when when they
are not as big but it's really really
good that we we are able to just access
this model for free right and and and
here this this is a nice H chart and we
can see for example the quality versus
price so we have this idiogram model
that it is quite good but it is more
expensive and now we have this flax
Chanel model that is just in terms of
quality is quite high right but it's
just the cheapest and and that's what I
said it is even free in together AI I
don't know if probably till a certain
limit so probably you cannot use this
model in in an application that serves
many many user but if it's just for your
own application if you are just
learning or and you want to integrate a
a text to image model you have it for
free and and I want to give you this
very quick very brief overview of
together AI because I've been using the
platform for for a long time already so
especially for for using the the the
flax models but I want to also take the
this time to to explain you this thing
that I've mentioned I think in this
video and in previous videos which is
what is an inference provider what is an
inference platform and it's just that
right so it's just a platform that
provides inference for you to run
different models and it does that via um
an API right so via different endpoints
in which you can take for example the
deeps R1 model that was so trending so
you can just take this model super super
easily and and they update um so they
are always U keep keeping up with the
new with the latest models and and you
can just take it and you can test
everything out by um getting here so in
the in the in the platform itself and in
the in the playground you can test chat
models you can test language models
image models and even audio
transcription models so yeah 100%
recommend this platform and finally to
Code Overview
finish up with this video let me show
you where in the project you can see the
the code related to to these two things
so you have um this directory called
image within modules in which we have
the image to text file so the the image
to text module and the text to image
module and they are again very
self-explanatory so the image to text
module what it does is um we use Gro as
we told you and we use the model um Lama
as you can see here yeah Lama 3.2 90
billion Bion
model so we use this model and we use
directly the The Grog API to use ask
this model to give us a description of
the image just simply that and and for
that we have this class called image to
text super super simple and as for the
text to image part we also have a text
to image module and a text to image
class and here what we do is before
actually doing the the text to image
what we need is that text right or we
need the prompt um to to be given to to
the flax model and what we do is we have
this create a scenario um function in
which we use a prompt which is the image
scenario prompt to guide the model into
creating for us uh an image prom so that
um is then used by the flx model to
generate the image right so this is so
you can see this at your own pace by
just downloading or just cloning the
repo just getting into our GitHub which
the link is down below in the
description but essentially what we ask
the model is to generate a visual prompt
that captures the scene that we that you
are describing right because remember we
use um the whole conversation to guide
the generation and also the ABA Uh
current activity and the output of it
would be something like a well both the
narrative that would be used for for for
the answer and the image prompt that
would be used to generate that answer
and this is something like atmospheric
Sunset scenes right it's just a text
description of an image then you can
just simply see how
we use the generate image function that
um what it does is we use the together
together
client and just
directly the the flax snail free model
and we just set a couple of parameters
like the width and the and the height of
the image and we just get that image
back then we just um send this via
WhatsApp and that would be all for
today's video so I hope you like the
video and if you did please give it a
like and also just let me know in the
comments just something that wasn't
clear something that you want me BBE to
go deeper in a different separate video
and I'll and I'll get on and I'll do
that so yeah bye-bye

### WhatsApp AI Agent Tutorial 6: Ava Installs WhatsApp

Intro
Hello everybody and welcome to lesson
six of Ava the WhatsApp agent. This
lesson is actually the last one and by
the end of it you're going to be able to
communicate or to talk with your agent
via WhatsApp and for that we are going
to just do a couple of things. So this
lesson is going to be quite uh short. So
firstly we are going to be looking at
this diagram that I have prepared in
which I will explain you more or less
how WhatsApp cloud works and how uses
web hooks to actually communicate with
your um API because actually um Ava is
being served by an API. I'm going to
explain you just a little bit about that
later. Also by showing you the code
everything is going to be very very
clear. And also something that um I will
show you how to do is how you actually
need to set everything up in the
developers um Facebook app. And by just
following everything that I'm going to
show you in this video, you're going to
be able to just replicate it and just
set it up for yourself very very easily.
WhatsApp webhook diagram
So let's start then by looking at this
simple diagram that I have prepared. And
in this diagram I just want to show you
and I want you to understand how um
WhatsApp intermediates in this whole
connection right in how you talk via
WhatsApp with with the agent. So what we
have here starting from the top is just
a user. So that could be you via
WhatsApp via your phone. You're going to
be sending them a message to WhatsApp
and then WhatsApp is just going to call
or it's going to send a request to the
application. And this whole thing that I
just explained, right? So a message
comes and then an HTTP request is
triggered. So that is actually called a
web hook. So a web hook is just an HTTP
HTTP call that is triggered by an event.
So in the case of um the WhatsApp web
hook, that event is the message that
arrives from the user. And now this HTTP
request has to be received by an API,
right? And what we have here is just um
an explanation like very brief or very
simple explanation of or visualization
of how we have set it up. So what we
have is um Ava that is a python
application that is actually uh served
via an API. We use a fast appy for it
just to expose an endpoint. Um I think
we call it WhatsApp web hook that then
can receive this HTTP request and then
it just decomposes you all the arguments
although that would be the important one
would be the message from the user which
user right or which phone number and
then it's going to be using all these
different services that we have
discussed and touched in the previous
lesson. So quadran for um for the memory
for the long-term memory grog for all
the inference 11 laps for the the
generation of the voice together AI for
the generation of the image. So once we
have used all these elements and we will
send back an HTTP response that would be
received by uh the WhatsApp cloud and
then an AI message right or or the
message from uh the the chatbot or AVA
will be received by the user. So that
would be me and and that is really all
right. So again right a web hook is just
an HTTP call that is triggered by an
event and in the case of WhatsApp that
is a user message and something here
that I haven't touched on is well these
two things. So I've already said that we
have an API that is a Python process. We
know about langraph right? Langraph is
the brain the the graph that actually
just decides what to do right so that is
the agency of the of of here of aba or
of our system and also what we have here
is just the symbol of docker because we
have dockerized this image you're going
to be able to look that up in the gith
repository you have everything I'm also
going to show you a bit later just the
code but yeah the application is
containerized so that it is easily
deployed on any cloud provider so
Actually, we went for a Google Cloud Run
and
Miguel in his newsletter, which again is
also linked down below. It's going to
give you a really good overview how to
set it up. But in this video, instead of
just deploying everything on cloud
provider, which will take a long time,
instead I'm going to be using Enro,
which if you don't know is an amazing
super useful tool for yeah, for testing
purposes, I think. So you wouldn't be
used in in production environments but
for testing is really good because what
it does it it is it provides a public
URL for you to test your local uh web
server and it does it by just creating a
tunnel from your local API. Right? So
maybe this is still not very clear but
once I show you that running in the code
everything is is going to make much more
Setting up app using Docker and ngrok
sense. So now in order for you to
actually be able to communicate via
WhatsApp with your agent, you have to do
two things. So first of all is for you
to have your API running. So your fast
app running and exposed via HTTPS. H
this is going to be done locally via
docker. So right now the repo is just
super simple like you just need to
docker compos app. And then with enro we
are going to expose the port of uh the
API. I'm going to show you that in a
second. And secondly, you have to
configure the web hook via this website
developersface.com. I'm going to show
you again. So I'm going to show you that
in a second as well. And you just need
to configure uh this web hook to be
pointing at the URL that you're going to
get by using enro. So let's jump into it
and you're going to see how easy it is.
So this is the GitHub repo of AI
companion. So this is just the repo that
I've been showing you always. And here
what we have is um under interfaces we
have WhatsApp and we have the WhatsApp
endpoint which is just simply how or
where we instantiate the fast API class
and then we include a router with the
WhatsApp router and if we go here it's
just simply the an API router which has
just a single endpoint that we have here
which is the WhatsApp handler and we
actually call this endpoint WhatsApp
response and it accepts the methods get
and post and this is just where we
define the whole um logic. It is not
very uh difficult. So you can you can
have a look at it. So you can so you can
have a look at in 3D use by checking the
ripple which is in the description
below. But maybe one of the methods that
we can have a a quick look at is going
to be the send response. Right? So this
is the method that we use to send the
response to the user via the WhatsApp
API. And this WhatsApp API is just
simply just a URL right so this is graph
Facebook.com so this is version 21 and
here we have to say so to which phone
number so this is this phone number we
can get it from developers Facebook and
WhatsApp actually provides a free uh
test number for you I think yeah that
you can just use it I think indefinitely
but again only for testing purposes and
then in production you would need to buy
a phone and just set it up but that
which should be very very simple and
then you just use the messages endpoint
and here you send the headers and the
JSON data. So and this JSON data would
just have the response text and actually
we don't we don't need these prints
anymore. I think this was just for for
for debugging at some point. Um and then
the other thing that is inter important
of course to know is just the headers.
In the headers we also have the
authorization. So the authorization
which is just a token. So I'm going to
tell you now I'm going to show you now
how you can get this token and with this
token and and the appropriate phone
number only with those two things you
will be able to just get this piece of
code from the repo and then you will be
able just to run it because because it's
it's really very simple. Now that we
have processed everything, we have gone
ourselves through our through the
WhatsApp documentation and now
everything is just in a very tidy and
well doumented Python file. So you will
see that it's very simple to use and
just adapted to your own agent. So this
file is the only one that you have to
actually just review to understand the
WhatsApp logic. Again, super simple. And
now we just need to do docker compose
app and maybe minus d just to have it in
the background. And so for that we just
um are instantiating or starting all the
servers and this shouldn't take too
much. Okay, good. Now we have seen that
um the three services are already up and
running. So we so locally we instantiate
a a quadrant server via um just the
docker image. We also have a chain lead
user interface for use for you to be
able to use chat with ABA via chain
lead. So via I use a web interface and
also of course we have the WhatsApp API
running. And now for us to be able to
see
which h port is being exposed. We can
just have a look at it here which is
yeah the WhatsApp service we have the
port 8080. So this is the portal we want
to expose via engro and we do that by
just um using the enro command which is
enrog okay and we have it here. So enro
http now you select the domain that you
that you have or that your user account
is going to have and then you select the
port. So that is 8080. So if we click
enter we and we can see here h the
tunnel being done right. So we can see
here that Enro is exposing this domain
and this is actually tunneling our local
host AD80. So now this is working. Let's
Configure webhook in developers.facebook.com
just have a look at developers Facebook.
And now the second thing which is to
configure that web hook to be looking or
to be pointing at this angro URL that we
now have. So you should go to
developers.fas.com.
So once you're here, you should go on on
the corner here. You should click on my
apps which is going to bring you to this
view. So here you're going to be able to
see all your apps. Of course, if you
haven't created an app. So if if this is
your first time, you have to click on
this bottom create an app and and just
complete a couple of details about the
app name and so on. So this will take
little. So in my case, I already have
that created. So I can just go into AI
companion
which takes me to this site. Okay. So
here I can see the AI companion app and
here we already so I already have
configure WhatsApp and this this is
where you want to go. So you have to go
to WhatsApp and then you have two
important things. So you have the API
setup and then the configuration. So let
me just briefly tell you what are the
important things here in the API setup.
Of course, one of the most important
things is what we have here on top,
which is the access token that we said
before that we need that for for
actually be able to authorize the
communication. So, you can just create
or generate an access token.
So, you have to log in or or relog or
reauthorize. So, once you have it, you
can just copy that and then you can just
paste it on the M file in your repo. But
also here you have another thing which
is actually quite nice. So before
actually setting up the WhatsApp web
hook, you can just test if you can
receive a message from this test number.
So this is something that I usually like
to do. So you have here the test number
that has been provided by WhatsApp for
you to test this application. And also
here you have the two. So is in the two
where you want to set up your phone. So
let me just put mine.
And what you have here now is that HTTP
post method that we have to or that we
are integrating as well in our
application. But this is just with kind
of like a a hello world. So we can just
send this message and now we can check
in WhatsApp if we actually have received
it. Okay. So this is Ava and my
conversation with her and yes indeed I
have received the hello world message.
So then this is set up. This is good.
Now the next thing that we have to set
up is just the web hook. So for that you
can click on configure web hooks here or
in configuration is just the same thing
which takes us to this side and here
just a couple of things that are
important. You have to make sure that
the messages h endpoint or how how do
you call the message field is enabled.
So it's you are subscribed to this one.
So the version really 21 22 doesn't
matter. I guess the 22 is just a recent
one. And something else that you want to
do in production is you want to set a
permanent token. But just for now,
right, we are testing the the token that
we generated before that suffices. And
here we have the call back URL. So So
this is the the enro URL that we were
getting from before, right? You remember
this URL. So it's just this one plus
also a slash WhatsApp response which is
the endpoint that we created right and
then the only the also another thing
that you have is just the very first
time that you set this up you want to
set a verify token so this could be just
a random string so it doesn't matter so
this is just to verify the connection
the very first time and actually we have
that in the code already so you'll see
that part of the code you see in
WhatsApp response here if get. So here
we just have the verify token. So in the
same way you also have to set it up in
the m. So let me just open m example
which is the the a template for you to
just put all the API keys and all the
environment variables that you need. So
here the WhatsApp verify token that that
would be just uh that that string that
you have to set up. Then the WhatsApp
token that is actually the access token.
So this is the important one the long
one. And then the WhatsApp phone number
ID which I think I haven't told you what
it is. So let me just show you. So that
WhatsApp phone ID that is this ID right?
So we have the test number which is
actually the the number that you would
use in WhatsApp to text this um the
agent and also here what you have is the
H the ID. So you just want to copy this
one, right? And just put in your m ID
the verify token. That would be
something that again you can just put
whatever you want. So that could be
something like for example aa agent
doesn't matter but you have to put the
same one in the verify token. Once set
up the verify token you can just click
verify and save. This is going to set it
up. But in my case I I have already
verified this connection so I don't need
to do that. And now and also of course
the the other thing that you need is
again the the token that is a token that
generates I think it lasts only two
hours unless you create a permanent one.
So once you create it here you can just
copy it go to your IDE and just paste it
right so not in the do example. So this
is just an example you would need to put
that in the M. So I'll do it myself.
Okay. I've just updated the WhatsApp
token also in my M file. So something
that I want to do is restart
the services because I want to take the
last uh so the last version of the M. So
for that we have to docker compose app
and docker comp. So docker compost app
and docker compose app again
restarted. So that is now started and
running again. So so now I should be
able to talk with Ava via WhatsApp. So,
let me just say hello you
and there we get the answer, right? So,
hey Jesus, what's up? Didn't expect to
hear from you so soon.
Good. And also, she remembers my name,
right? Because we have this long-term
memory and she remember she remembers my
name, which is crazy. So, so yeah, it
worked well. So, now I'm I'm I should be
able to just to have a conversation with
Aba like always, and it's just working.
Outro
Okay, and that concluded uh this lesson
and actually the course as well. So,
it's been six weeks, six lessons with a
lot of information and and I think a lot
of value. So, we really hope that you
enjoy this this course that you learn a
lot of things and I would love to see in
the comments below what are the projects
that you want to build or that you are
going to build now that you have learned
all these things. I would really really
like to hear from you. And of course, if
you like this kind of content, if you
want to be updated in everything that is
happening in the field of AI, just
remember to subscribe to my channel and
also give it a like. I would actually
appreciate that a lot. And yeah, that
will be all. Bye-bye. See you in another
one.
