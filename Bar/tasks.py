from celery import task

@task()
def send_fidelity():
    print "pouet"
    return True