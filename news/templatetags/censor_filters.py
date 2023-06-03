from django import template
 
register = template.Library() 

bad_words = ['fuck', 'piss', 'shit', 'cunt', 'motherfucker']
    
@register.filter(name='censor') 

def censor(testText):
    
    for word in bad_words:
        testText = testText.lower().replace(word.lower(), '***') 
    return testText