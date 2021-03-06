## Data Integrity

[Set Up Server](#head1) | [Set Up Clients](#head2) | [Register Users](#head3) | [Sign Data](#head4) | [Find the Sender's Card](#head5) | [Verify Data](#head6)

Use **Virgil** to verify the integrity of data at any point. **Data Integrity** is essential to anyone who wants to guarantee that their data has not been tampered with.


<!-- ![Virgil Signature Intro](/img/Signature_introduction.png "Data integrity") -->

## <a name="head1"></a> Set Up Server
Your server should be able to authorize your users, store Application Virgil Key and use **Virgil SDK** for cryptographic operations or for some requests to Virgil Services. You can configure your server using the [Setup Guide](/documentation/guides/configuration/server.md).


## <a name="head2"></a> Set Up Clients
Set up the client side to provide your users with an access token after their registration at your Application Server to authenticate them for further operations and transmit their **Virgil Cards** to the server. Configure the client side using the [Setup Guide](/documentation/guides/configuration/client.md).


## <a name="head3"></a> Register Users
Now you need to register users. We need to create a Virgil Key and Card for each user that will be sending verified data. Cards are stored with Virgil and contain your user's public encryption keys.

![Virgil Card](/documentation/img/Card_introduct.png "Create Virgil Card")

When we have already set up the Virgil SDK on the server & client sides, we can finally create Virgil Cards for the users and transmit the Cards to your Server for further publication on Virgil Services.


### Generate Keys and Create Virgil Card
Use the Virgil SDK on the client side to generate a new Key Pair, and then create a user's Virgil Card using the recently generated Virgil Key. All keys are generated and stored on the client side.

In this example, we will pass on the user's username and a password, which will lock in their private encryption key. Each Virgil Card is signed by a user's Virgil Key, which guarantees the Virgil Card's content integrity over its life cycle.

```python
# generate a new Virgil Key
alice_key = virgil.keys.generate()

# save the Virgil Key into the storage
alice_key.save("[KEY_NAME]", "[KEY_PASSWORD]")

# create identity for Alice
alice_identity = virgil.identities.create_user("alice")

# create user Virgil Card
alice_card = virgil.cards.create(alice_identity, alice_key)
```

**Warning**: Virgil doesn't keep a copy of your Virgil Key. If you lose a Virgil Key, there is no way to recover it.

It should be noted that recently created user Virgil Cards will be visible only for application users because they are related to the Application.

Read more about Virgil Cards and their types [here](/documentation/guides/virgil-card/creating-card.md).


### Transmit the Cards to Your Server

Next, you must serialize and transmit this cards to your server, where you will approve & publish Users' Cards.

```python
# export a Virgil Card to string
exported_card = alice_card.export()

# send Virgil Card to server
send_to_srv(exported_card)
```

Use the [approve & publish users](https://github.com/VirgilSecurity/virgil-sdk-python/blob/v4/documentation/guides/configuration/server.md#-approve--publish-cards) guide to publish users Virgil Cards on Virgil Services.

## <a name="head4"></a> Sign Data

With the sender's Cards in place, we are now ready to ensure the Data Integrity by creating a **Digital Signature**. This signature ensures that the third party hasn't modified messages' content and you can trust a sender.

```python
# prepare a message
message = "Hey Bob, hope you are doing well."

# wrap data to buffer
data_buff = VirgilBuffer.from_string(message)

# generate signature
signature = alice_key.sign(data_buff)
```

To create a signature, you need to load Alice's Virgil Key. The [Loading Key](/documentation/guides/virgil-key/loading-key.md) guide provides more details.

### Transmission

The Sender is now ready to transmit the signature and message to the Receiver.

See our guide on Transmitting Data for best practices, or check our tutorial on [Secure IP Messaging with Twilio](https://github.com/VirgilSecurity/virgil-demo-twilio).


## <a name="head5"></a> Find the Sender's Card

For the receiving client to verify the message it needs the sender's Virgil Card.

To look up the sender's card we use the identifier we used when publishing the card, in this case that is `alice`.

```python
# search for all User's Virgil Cards.
alice_cards = virgil.cards.find(["alice"])
```

The identifier for a Virgil Card can be any ID you prefer, for example, a username or user ID. The [Finding Card](/documentation/guides/virgil-card/finding-card.md) guide provides more details.

This will return all cards for Alice, which we can use to verify the data.


## <a name="head6"></a> Verify Data

With the sender's Cards in, we can now verify ensure the Data Integrity of the message by checking the Digital Signature.

```python
# verify signature using Alice's Virgil Card
if not alice_cards.verify(message, signature):
    raise Exception("Aha... Alice it's not you.")
```

To create a signature, you need to load Alice's Virgil Key. The [Loading Key](/documentation/guides/virgil-key/loading-key.md) guide provides more details.
