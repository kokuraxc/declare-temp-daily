# declare-temp-daily

It's such a hassle **to declare the temperature to the company twice every day**. And I tend to forget to do so from time to time. This piece of Python program will do this boring chore for me and my wife.

## Prerequisites
* [Selenium](https://selenium-python.readthedocs.io) will be used to do the job.
* [schedule](https://pypi.org/project/schedule/) is used to run the task twice daily.

```bash
pip install selenium
pip install schedule
```

## Run the code

```bash
python auto_selenium.py
```
The program will open a Chrome window in Incognito mode, log into the company website, and then update the temperature.

## Note
* Linting using `flake8` and `pydocstyle`.
* I hided the `url`, `user` and `password` in the `.config` file.

```json
{
    "url": "YOU_URL",
    "user": "YOUR_USER_NAME",
    "password": "YOUR_PASSWORD"
}
```
---
## Logs

### **Log #1: Oct 04, 2020 2:59 PM**

Last night I roughly finished the functions of using Selenium to submit the temperature. Only that there was a problem: it will fail and produce an error when Selenium clicks the "Submit" button.

![](submit-error.png)

When I do the inputs and clicks manually, there would be no such errors.

I guessed it might be because the web page I'm accessing detects the other party is an automated program, but no real humans. So it refuses to cooperate. 

A simple Google search leaded me to this stack**overflow** post [*Can a website detect when you are using selenium with chromedriver?*](https://stackoverflow.com/questions/33225947/can-a-website-detect-when-you-are-using-selenium-with-chromedriver#41220267) 

I didn't read through the post, but this did confirm my hypothesis. So I got my hands dirty to read the page source. And luckily I found the following JavaScript snippet.

```JavaScript
function detectWebdriver(){
    try{
        if(navigator.webdriver){
            document.dlytemperature.webdriverFlag.value ="Y";
        }
    }catch(err){} 
    
    try{
        if(window.document.documentElement.getAttribute("webdriver")){
            document.dlytemperature.webdriverFlag.value ="Y";
        }
    }catch(err){}
}
```

Now that I know the cause, I'll begin working on it!

### **Log #2: Oct 05, 2020 4:20 PM**

Added a configuration file, from which the program will read the URL, user name and password. Also extracted the function into a method, so later can ease the process of calling it.

### **Log #3: Oct 07, 2020 7:31 PM**

I added in the [schedule](https://pypi.org/project/schedule/) package by `Daniel Bader` to run the task every day in the morning and afternoon.

Looking at the examle code, it's so easy to schedule a task with this package.

```python
import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```