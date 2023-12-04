# Homework: Module 8 - NoSQL databases

## 1st Task

### Input Data
We have a json file with authors and their properties: date and place of birth, a brief description of the biography.

### Contents of the `authors.json` file.

[
  {
    "fullname": "Albert Einstein",
    "born_date": "March 14, 1879",
    "born_location": "in Ulm, Germany",
    "description": "In 1879, Albert Einstein was born in Ulm, Germany. He completed his Ph.D. at the University of Zurich by 1909. His 1905 paper explaining the photoelectric effect, the basis of electronics, earned him the Nobel Prize in 1921. His first paper on Special Relativity Theory, also published in 1905, changed the world. After the rise of the Nazi party, Einstein made Princeton his permanent home, becoming a U.S. citizen in 1940. Einstein, a pacifist during World War I, stayed a firm proponent of social justice and responsibility. He chaired the Emergency Committee of Atomic Scientists, which organized to alert the public to the dangers of atomic warfare.At a symposium, he advised: \"In their struggle for the ethical good, teachers of religion must have the stature to give up the doctrine of a personal God, that is, give up that source of fear and hope which in the past placed such vast power in the hands of priests. In their labors they will have to avail themselves of those forces which are capable of cultivating the Good, the True, and the Beautiful in humanity itself. This is, to be sure a more difficult but an incomparably more worthy task . . . \" (\"Science, Philosophy and Religion, A Symposium,\" published by the Conference on Science, Philosophy and Religion in their Relation to the Democratic Way of Life, Inc., New York, 1941). In a letter to philosopher Eric Gutkind, dated Jan. 3, 1954, Einstein stated: \"The word god is for me nothing more than the expression and product of human weaknesses, the Bible a collection of honorable, but still primitive legends which are nevertheless pretty childish. No interpretation no matter how subtle can (for me) change this,\" (The Guardian, \"Childish superstition: Einstein's letter makes view of religion relatively clear,\" by James Randerson, May 13, 2008). D. 1955.While best known for his mass-energy equivalence formula E = mc2 (which has been dubbed \"the world's most famous equation\"), he received the 1921 Nobel Prize in Physics \"for his services to theoretical physics, and especially for his discovery of the law of the photoelectric effect\". The latter was pivotal in establishing quantum theory.Einstein thought that Newtonion mechanics was no longer enough to reconcile the laws of classical mechanics with the laws of the electromagnetic field. This led to the development of his special theory of relativity. He realized, however, that the principle of relativity could also be extended to gravitational fields, and with his subsequent theory of gravitation in 1916, he published a paper on the general theory of relativity. He continued to deal with problems of statistical mechanics and quantum theory, which led to his explanations of particle theory and the motion of molecules. He also investigated the thermal properties of light which laid the foundation of the photon theory of light.He was visiting the United States when Adolf Hitler came to power in 1933 and did not go back to Germany. On the eve of World War II, he endorsed a letter to President Franklin D. Roosevelt alerting him to the potential development of \"extremely powerful bombs of a new type\" and recommending that the U.S. begin similar research. This eventually led to what would become the Manhattan Project. Einstein supported defending the Allied forces, but largely denounced the idea of using the newly discovered nuclear fission as a weapon. Later, with Bertrand Russell, Einstein signed the Russell-Einstein Manifesto, which highlighted the danger of nuclear weapons."
  },
  {
    "fullname": "Steve Martin",
    "born_date": "August 14, 1945",
    "born_location": "in Waco, Texas, The United States",
    "description": "Stephen Glenn \"Steve\" Martin is an American actor, comedian, writer, playwright, producer, musician, and composer. He was raised in Southern California in a Baptist family, where his early influences were working at Disneyland and Knott's Berry Farm and working magic and comedy acts at these and other smaller venues in the area. His ascent to fame picked up when he became a writer for the Smothers Brothers Comedy Hour, and later became a frequent guest on the Tonight Show.In the 1970s, Martin performed his offbeat, absurdist comedy routines before packed houses on national tours. In the 1980s, having branched away from stand-up comedy, he became a successful actor, playwright, and juggler, and eventually earned Emmy, Grammy, and American Comedy awards."
  }
]

We also have the following json file with quotes from these authors.

### Contents of the `quotes.json` file.

[
  {
    "tags": [
      "change",
      "deep-thoughts",
      "thinking",
      "world"
    ],
    "author": "Albert Einstein",
    "quote": "'The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.'"
  },
  {
    "tags": [
      "inspirational",
      "life",
      "live",
      "miracle",
      "miracles"
    ],
    "author": "Albert Einstein",
    "quote": "'There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.'"
  },
  {
    "tags": [
      "adulthood",
      "success",
      "value"
    ],
    "author": "Albert Einstein",
    "quote": "'Try not to become a man of success. Rather become a man of value.'"
  },
  {
    "tags": [
      "humor",
      "obvious",
      "simile"
    ],
    "author": "Steve Martin",
    "quote": "'A day without sunshine is like, you know, night.'"
  }
]

### Order of execution
1. Create an Atlas MongoDB cloud database
2. Using ODM Mongoengine, create models to store data from these files in the authors and quotes collections.
3. When storing quotes, the author field in the document should not be a string value, but the Reference fields field, where the ObjectID from the authors collection is stored.
4. Write scripts to upload json files to the cloud database.
5. Implement a script to search for citations by tag, author name or set of tags. The script is executed in an infinite loop and accepts commands in the following format using the usual input operator - command: value. Example:
  * name: Steve Martin — find and return a list of all quotes by the author Steve Martin;
  * tag:life — find and return a list of quotes for the life tag;
  * tags:life,live — find and return a list of quotes with life or live tags (note: no spaces between life, live tags);
  * exit — end the execution of the script;
6. Output of search results only in utf-8 format.

## Additional Task

7. Consider and implement for the name:Steve Martin and tag:life commands the ability to write abbreviated search values as name:st and tag:li respectively;
8. Cache the result of the name: and tag: commands using Redis, so that when the search is repeated, the search result is not taken from the MongoDB database, but from the cache.
9. For the name:st and tag:li commands, use regular expressions in String queries.

## 2nd Task

Write two scripts: consumer.py and producer.py. Using RabbitMQ, organize with the help of queues the simulation of email distribution to contacts.

Using Mongoengine ODM, create a model for the contact. The model must contain fields: full name, email and a logical field that has a value of False by default. It means that the message to the contact has not been sent and should return True when sent. You can come up with other fields for the information load yourself.

When the producer.py script is run, it generates a certain number of fake contacts and writes them to the database. Then queues a RabbitMQ message containing the ObjectID of the generated contact, and so on for all generated contacts.

The consumer.py script receives a message from the RabbitMQ queue, processes it and simulates sending a message by email with a stub function. After sending the message, the logical field for the contact must be set to True. The script runs constantly waiting for messages from RabbitMQ.

### WIKI
Stub function - a function that does not perform any meaningful action, that returns an empty result or input data in an unchanged form. Same as method stub.

A stub can mimic the behavior of existing code (for example, procedures on a remote computer) or be a temporary replacement for code that has not yet been created. For example, instead of a function that performs complex calculations, you can temporarily (until the function itself is written) put a stub that always returns 1, and debug other functions that depend on it.

## Additional Task

Enter an additional field — phone number — in the model. Also add a field that is responsible for the best way to send messages - SMS by phone or email. Let producer.py send SMS and email contacts to different queues. Create two scripts consumer_sms.py and consumer_email.py, each of which receives and processes its contacts.
