# HTTPager

An HTTP pager service that can be connected to different channels. When the pager's URL is called, the message is dispatched to all of its channels (currently Gmail, Telegram, and Slack available).

This is inspired by [Knock Knock](https://github.com/huggingface/knockknock), but instead of having to integrate Python code, HTTPager lets you simply make an HTTP call (using cURL, for example). As long as the machine can make an HTTP call to an external server, it can page you. **No need to configure email or other messaging services on every machine you administer.** Once you have your **Pager URL**, no more configuration is needed on any machines that will page you. They simply make a cURL GET or POST call to pager URL. There is no authentication when calling a pager; make sure you keep the Pager URL secret if you don't want to be paged by others.

## Use cases

- You run `apt-update; apt-get upgrade` and want to step away from the terminal. Simply add `apt-update; apt-get upgrade; pageme upgrade finished` to the end of the command and you'll get a page on any channel connected to your pager (my favourite is Telegram) when the upgrade completes.

- A use-case from [Knock Knock's README](https://github.com/huggingface/knockknock):  
  >"When training deep learning models, it is common to use early stopping. Apart from a rough estimate, it is difficult to predict when the training will finish. Thus, it can be interesting to set up automatic notifications for your training. It is also interesting to be notified when your training crashes in the middle of the process for unexpected reasons."

## Deployment using Heroku

Make sure you have the [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) installed.

```
git clone https://github.com/alexandres/HTTPager.git
cd HTTPager
heroku create <yourfunappname>
git push heroku master
heroku run python manage.py createsuperuser
# type in your username, email, and password
heroku config:set SECRET_KEY=$(openssl rand -base64 64)
```

Now access the admin site at https://yourfunappname.herokuapp.com/admin/ using the username and password you created above to make sure everything is loading correctly.

## Creating Pagers and Channels

Pagers and channels are created using the admin interface  at https://yourfunappname.herokuapp.com/admin/.

Before creating a Pager, you'll need to setup at least one channel. 

### Channels

You can use any name for the channels. It's simply to help you identify them in the admin interface.

*Quoted instructions below from from [Knock Knock's README](https://github.com/huggingface/knockknock)*.

#### Email

> You'll need a gmail email address to use it (you can setup one [here](https://accounts.google.com), it's free). I recommend creating a new one (rather than your usual one) since you'll have to modify the account's security settings to allow the Python library to access it by [Turning on less secure apps](https://devanswers.co/allow-less-secure-apps-access-gmail-account/).

Create a new Gmail channel at https://yourfunappname.herokuapp.com/admin/pager/gmailchannel/add/ using the email and password of the **sender** account you just created, and add the **recipient** email address which will be paged.

#### Telegram

> You can also use Telegram Messenger to get notifications. You'll first have to create your own notification bot by following the three steps provided by Telegram [here](https://core.telegram.org/bots#6-botfather) and save your API access `TOKEN`.

>Telegram bots are shy and can't send the first message so you'll have to do the first step. By sending the first message, you'll be able to get the `chat_id` required (identification of your messaging room) by visiting `https://api.telegram.org/bot<YourBOTToken>/getUpdates` and get the `int` under the key `message['chat']['id']`.

Create a new Telegram channel at https://yourfunappname.herokuapp.com/admin/pager/telegramchannel/add/ using the token and chat id you created above.

#### Slack

> Similarly, you can also use Slack to get notifications. You'll have to get your Slack room [webhook URL](https://api.slack.com/incoming-webhooks#create_a_webhook).

Create a new Slack channel at https://yourfunappname.herokuapp.com/admin/pager/slackchannel/add/ using the webhook URL and channel name (type in channel with hashtag, ie. #channelname). 

#### Pagers

Create a pager at https://yourfunappname.herokuapp.com/admin/pager/pager/add/ by giving it a name, a slug, and selecting the channels to which messages should be sent.

A slug is automatically generated, but you can give it an easier to remember value. 

### Using Pagers

You *page* your pager by making a GET or POST call to https://yourfunappname.herokuapp.com/pager_slug. If the automatically generated slug is `bc2c747607a564a04d11323d7f36838b`, the **Pager URL** would be https://yourfunappname.herokuapp.com/bc2c747607a564a04d11323d7f36838b . Any GET and POST variables are included in the message sent to channels.

Example: you are training a ML model and would like to be paged when it completes,

```
python train_model.py; curl -G https://yourfunappname.herokuapp.com/bc2c747607a564a04d11323d7f36838b --data-urlencode "subject=Finished training model!"
# ; ensures curl is run even if there's an error during training
# -G is necessary to encode (in case contains spaces for example) and append subject to query string
```

I have the following handy function in my `.bashrc` file:

```
function pageme {
    curl -G https://yourfunappname.herokuapp.com/bc2c747607a564a04d11323d7f36838b --data-urlencode "subject=${*}"
}
```

The previous script then becomes:

```
python train_model.py; pageme Finished training model\!
```

## TODO

Pull requests are very welcome!

- [ ] "Test" button with admin interface for testing channels.
- [ ] Better message formatting (currently just sends GET and POST dicts).

## License

Copyright (c) 2019 Salle, Alexandre <alex@alexsalle.com>. All work in this package is distributed under the MIT License.

