import csv   # to read csv file
from selenium import webdriver

def readCSV():
    # list to read the details from
    country_name=[]
    validity_begins=[]
    license_plate=[]
    powered_by=[]
    type_of_Vignette=[]
    with open("sample.csv",mode="r") as file:  # opening and reading the file
        sampleFile=csv.reader(file)   # reads the lines from the file
        for lines in sampleFile:
            #print(lines)
            country_name.append(lines[0])
            validity_begins.append(lines[1])
            license_plate.append(lines[2])
            powered_by.append(lines[3])
            type_of_Vignette.append(lines[4])
    with open("config.txt",mode="a") as file2:
        configfile = file2.readlines()
    placingOrder(configfile,country_name,validity_begins,license_plate,powered_by,type_of_Vignette)

def placingOrder(configfile,country_name,validity_begins,license_plate,powered_by,type_of_Vignette):
    driver = webdriver.Firefox()    # opens search engine as firefox
    driver.get("https://edalnice.cz/en/bulk-purchase/index.html")   # opens the website to be operated
    for x in range(0,5):
        driver.find_elements_by_name("Vehicle’s country of registration")  # find the label with name 
        driver.send_keys(country_name[x])   # enters the value from the list created to the entry box
        driver.find_elements_by_name("Beginning of vignette validity")
        driver.send_keys(validity_begins[x])
        driver.find_elements_by_name("License plate number (0)")
        driver.send_keys(license_plate[x])

        driver.find_elements_by_xpath('//*[@id="root"]/div/form/div/div[1]/div/fieldset/div/div/div')  # find the powered by button with the xpath(using inspect)

        # selects button if there is info in the csv file
        if powered_by !="":
            if powered_by == "Natural gas":
                checkboxElement = driver.find_element_by_id("Natural gas")
                checkboxElement.click()
            else:
                checkboxElement = driver.find_element_by_id("Biomethane")
                checkboxElement.click()
                
        # finds the button for adding new batch and click to add if the exist elements
        if x!=5:
            l = driver.find_element_by_xpath("//button[text()='+ADD NEW BATCH ']")
            l.click()
            driver.close()
        else:
            c = driver.find_elemnets_by_name("CONTiNUE")
            c.click()
            d = driver.find_elemnets_by_name("CONTiNUE")
            d.click()
    
    # first part of payment
    driver.find_elements_by_name("Email")
    driver.send_keys(configfile[0])
    driver.find_elements_by_name("Email again for review")
    driver.send_keys(configfile[0])
    payment = driver.find_elements_by_name("Via payment card")
    payment.click()
    checkboxelement = driver.find_elements_by_xpath("//*[@id="multiEshop"]/div[1]/div/fieldset[1]/div[3]/div")
    checkboxelement.click()
    e = driver.find_elemnets_by_name("PAY")
    e.click()
    
    # for the payment 
    def payment(configfile):
        driver.find_elemnets_by_name("Card number")
        driver.send_keys(configfile[2])
        driver.find_elemnets_by_name("Validity")
        driver.send_keys(configfile[3])
        driver.find_elemnets_by_name("CVC/CVV")
        driver.send_keys(configfile[4])
        f = driver.find_elemnets_by_xpath("//*[@id="creditcard"]/div[5]")  # using xpath as the button name will be changing everytime
        f.click()
        
    payment(configfile)