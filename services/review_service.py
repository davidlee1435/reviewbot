from gateways import review_gateway

def create_review(user, command, channel):
    pr_url = _extract_pr_url(command)
    print "Creating review for {0} from user {1}".format(pr_url, user)
    if not pr_url:
        return
    review_id = review_gateway.add_review(reviewee_id=user, reviewer_id=None, url=pr_url)
    return review_id

def _extract_pr_url(command):
    words = command.split()
    url = [word for word in words if "github.com" in word and "/pull/" in word]
    if not url:
        print "Url not in command!"
        return
    return url[0]

def get_review(review_id):
    return review_gateway.get_review(review_id=review_id)
