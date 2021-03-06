# Writing a small browser extension

When someone shares their Google Calendar with you but wants to hide
some details of an event from you, they can set it to 'private.' In
which case you'll see a little event that just says "busy":

![Image contents: an unadulterated private Google Calendar event. It just says "busy".](/static/img/normal-busy.png)

As ~~a joke~~ an art project, I decided to write a small browser extension
that makes it so that all events on your Google Calendar show up as
"busy":

![Image contents: a screenshot of my Google Calendar. All the events are marked "busy".](/static/img/all-busy.png)

<!-- image here -->

During the process, I learned a bunch of things:
* good artists copy; great artists steal
* MutationObserver is a cool and helpful thing
* ARIA roles are rad!!
* The difference between the `interactive` and `complete` loading states

It was really helpful to know that the [Calendar
Merge](https://github.com/imightbeamy/gcal-multical-event-merge) extension
exists and works. Unlike mine, it makes your calendar easier to use by messing
with the event display. This gave me faith that my idea was doable, and reading
the source helped me find a workable approach, which I shall detail forthwith.

Okay. So we want to grab all the events displayed on your calendar,
and replace their wonderful descriptive titles with "busy." Because
Google Calendar is doing all sorts of wacky data loading and mutation,
we can't want to just change all the events on page-load - the events
might not even have loaded in yet, and Google will probably change
them out from under us anyways. We want to make sure that, whenever
something changes on the page, we forcibly suppress any events that
are trying to revert to their natural state.

First, we want to instantiate a `MutationObserver` and have it observe
the `body` element:

```javascript
const observer = new MutationObserver(main);

observer.observe(
  document.querySelector('body'),
  { childList: true, subtree: true, attributes: true }
);
```

This does what the words say: we now have a stream of DOM mutations,
which we buffer and send to the callback `main` function every once in
a while.

The next thing we need to do is filter down these mutations so we can
see if there are any mutations we care about. My first inclination was
to use classnames, but those are totally obscured and I was worried
they could be changed out at any point. Fortunately, I cheated off the
Calendar Merge code and saw that they were using these weird
attributes like `role` and `aria-hidden`.

I decided to dig into this a little more - turns out that these are
attributes that screenreaders use to understand what UI function a DOM
element serves (ARIA stands for "Accessible Rich Internet
Applications"). This is pretty cool! Yet another instance of how
accessiblity helps everyone: these attributes make it super easy to
find the right elements to vandalize:

```javascript
const dialog = relevantMutations.filter(
  (node) => node.matches('[role="dialog"]')
);
```

Eventually I got the events to say "busy" instead of their real
titles. But there was still a problem: the real events would load in,
and it would take a few seconds to obscure all the information. This
is no good - in those few seconds I might learn what I was supposed to
be doing instead of writing this blog post!

I had a bunch of different theories but I wanted to make sure it
wasn't just loading in late. So I added a little `console.log` at the
top of my script, which showed that indeed, my MutationObserver wasn't
beginning its Observation until several seconds after the events were
displayed. 

I found that, in the extension's `manifest.json`, I could set when to
run my script. The options were `document_start`, `document_end`, and
`document_idle`. What do those mean? `document_start` means `loading`,
or "I've started loading the DOM;" `document_end` means `interactive`,
or "I've parsed the DOM but there's still some more stuff I need to
load;" and `document_idle` means `complete`, or "There's nothing else
to do and I'm bored." Browser extension scripts default to loading at
`document_idle`, and by setting mine to load at `document_end` instead
I was able to get rid of the delay. When I set it to load at
`document_start`, the `MutationObserver` couldn't find a `body` to
attach to, so nothing happened.

There's still a bunch of work to do on this: I need to actually
package the extension for distribution, and I'd like to make it
obscure even more information. But I've already learned a ton from
this experience! Here's the Github repo: [busybody](https://www.github.com/jdangerx/busybody)
