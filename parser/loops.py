def scholar_loop(scholar, coauthors, driver):
    print(f"getting {domain_name}{prefix}{scholar}")
    driver.get(f"{domain_name}{prefix}{scholar}")

    click_more(driver, wait)

    page = BeautifulSoup(driver.page_source, 'html.parser')

    #### CITATIONS SEARCH ##########

    print("CITATIONS SEARCH")
    print("looking for citations...")
    
    result = citation_search(page)

    print(f"we found {sum(result)} citations.")
    print(f"writing citations to {scholar}.csv...")

    save_citations(scholar, result)

    print("writing to file is DONE.")
    
    ### CO-AUTHORS SEARCH ###

    print("CO-AUTHORS SEARCH")
    print("looking for co-authors...")

    if coauthors_exist(driver):
        
        click_coauthors(driver)

        driver.implicitly_wait(5)

        for element in driver.find_elements(By.XPATH, "//h3[@class='gs_ai_name']/a"):
            coauthor_link = re.search("user=.{12}", element.get_attribute('href'))
            coauthor = re.sub("user=", '', coauthor_link.group(0))
            coauthor_already_exists = False

            if coauthor_link is not None:
                for i in range(len(scholars)):
                    if coauthor in scholars[i]:
                        print(f'user {coauthor} already exists in set on level {i}')
                        coauthor_already_exists = True
                        break

                if not coauthor_already_exists:
                    print(f'add {coauthor} to coauthors set...') #for search level {level+2}...')
                    coauthors.add(coauthor)# re.sub("user=", '', user_link.group(0)))

                    network.append((scholar, coauthor))

    else:
        print("this page does not have co-authors list")

