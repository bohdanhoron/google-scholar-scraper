def coauthor_scraped(coauthor, scholars) -> bool:
    for i in range(len(scholars)):
        if coauthor in scholars[i]:
            print(f'user {coauthor} already exists in set on level {i}')
            return True
        else:
            return False

