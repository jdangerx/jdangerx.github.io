# Rolling your own static site generator

Static site generators are cool! I think they're a great way to put
stuff on the internet, especially if you're not feeling the whole
Medium thing.

I've tried using a couple in the past, and nothing ever really stuck.
My problem was that I wrote blog posts slower than the site generator
teams wrote major releases. And instead of being a good boy and
pinning my versions, I would always upgrade and break my build.

So I decided to roll my own. How hard can it be? We just have to turn
a bunch of markdown files into HTML.

I bet it *can* get pretty hard, but it can also definitely be very
easy. Here are some ways that I made it easy:

- I use [Markdownit](https://markdown-it.github.io/) to render all the
  Markdown on the client side

- all of the templating is done with native Python format strings
  (yes, even the Atom feed!)

Let's talk about the client side rendering first. I saw this idea
floating around a couple years ago: just dump your markdown to the
client-side, and have some library in the browser render it to
something prettier. This has a couple benefits: it fails gracefully -
if someone wants to look at the site through `lynx` they can - and,
more importantly, means that I don't have to do any Markdown-specific
work on the backend. I just dump the source into a `<pre>` tag and
call it a day.

Next, all of the templating is done with Python format strings. This
one is pretty fun. For example, here's my Atom entry template:

```xml
<entry>
  <title>{title}</title>
  <link href="http://www.daz.zone/blog/{basename}.html"/>
  <id>md5:{md5}</id>
  <updated>{ctime:%Y-%m-%dT%H:%M:%S}</updated>
  <summary>{summary}</summary>
</entry>
```

Just read that in, call `.format(title="something", ...)` on the
string, and you're good to go! There's a little bit more machinery
involved if you need to repeat a section:

```python
# Feed template looks like this:
# <?xml version="1.0" encoding="utf-8"?>
# <feed xmlns="http://www.w3.org/2005/Atom">
# 
#   <title>DAZ.ZONE</title>
#   <link href="http://www.daz.zone/blog"/>
#   <updated>{generated_time}</updated>
#   <author>
#     <name>Dazhong Xia</name>
#   </author>
#   <id>http://www.daz.zone</id>
#   <subtitle>DAZ dot ZONE</subtitle>
# 
#   {entries}
# </feed>

def make_feed(with_metadata, entry_template, feed_template):
    generated_time = "{:%Y-%m-%dT%H:%M:%S}".format(datetime.now())
    entries = [
        entry_template.format(md5=md5.md5(entry["title"]).hexdigest(), **entry)
        for entry in with_metadata
    ]
    feed = feed_template.format(
        generated_time=generated_time,
        entries="\n".join(entries)
    )
    return feed
```

For my use-case, it doesn't really have to get fancier than that.

One more thing - it was pretty easy to generate an Atom feed with this
templating strategy. I did, however, run into a problem generating the
IDs for the entries. In the
[example](https://validator.w3.org/feed/docs/atom.html) we see those
being generated as UUIDs. However, I regenerate my entire feed every
time - so I needed something deterministic. I decided to hash the
titles instead, since I don't think I'll be changing titles very
frequently and I'm not really worried about hash collisions.

As you can see, there's still plenty of work that can be done - I
could add syntax highlighting, work on the styling and templates, and
so on - but I hope you can also see that this is totally servicable
also! In the end I think this took about as much time as it would have
taken me to get a normal static site generator set up, but I got a
blog post out of it as well.

Lastly, the Python code is less than 150 lines and can be found
[here](https://github.com/jdangerx/jdangerx.github.io/blob/master/generate.py).
The JavaScript is
[here](https://github.com/jdangerx/jdangerx.github.io/blob/master/static/blog.js).
