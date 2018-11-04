# TLA+: Maybe I would have sent fewer panicked messages to my PM

When I was applying to RC I didn't know what I really wanted to work
on. My friend Hillel kept going on about this "TLA+" thing, though.
What is it? I've been describing it briefly as a tool that finds weird
ambiguities and states that you overlooked when you were designing
your system. The classic use-case is reasoning through complicated
distributed systems - the major industry application I've heard of is
in orchestrating service architectures.

This sounded pretty helpful, so I decided to start off RC with it. I
started working through Hillel's book, [Practical
TLA+](https://www.apress.com/us/book/9781484238288).

After getting through the first half, a crash course in the specifics
of the language, I decided it was time to start using TLA+ on other
projects. But I kind of got stuck: I wasn't really planning on
implementing hard distributed stuff, and I didn't see how I could
apply it to the simpler projects I was actually thinking about. I
decided that I'd just finish out the book for kicks.

Fortunately the rest of the book that I had given up on was actually
all about applications and walked me through a lot of increasingly
complex examples. I gained a bunch of fluency in the language and
approach. By the end of the book, I'd learned a lot, and even got to
pretend to design MapReduce. Which brings me to the big question: I'm
not likely to be building a fancy distributed system, so will this be
useful for me ever?

## Yes

Yes. Here's an example. Due to poor behavior on my part, this scenario
played out pretty frequently at my old job:

1. Our team decides to build a feature.
   
2. Our responsible and professional product manager asks me, the
   engineer who owns the implementation, what I think about the
   various product requirements.

3. I read the product requirements and they make sense to me. I say,
   "sounds good."

4. ...

5. I push to production, realize that I had forgotten to think about
   the product implications of a specific edge case, and now some
   users are seeing some garbage or, like, committing fraud en masse
   or something.

6. I send my PM a slack message asking her how to handle that edge
   case but she's in meetings for the next week so the business goes
   under.
   
A few months later, I was working through an example in the book:
modeling "a library where people can check out, reserve, and return
books, where people eventually get to read the books they want to."

As I worked through a design of the system, I started running into the
ambiguities and contradictions embedded in that sentence: what does
"get to read" mean? How does a reservation work? And a lightbulb went
off in my head: if I had rigorously thought through the product
requirements at my old job, I could have avoided a lot of pain, even
though I wasn't building fancy distributed systems.

And as I was modeling the users as separate processes in the library
system, I had a thought: in a weird dehumanizing way, any system with
user interactions is a distributed system. So, yes, I expect to use
TLA+ to reason about distributed systems and save me a bunch of pain
in the future.
