start = "Welcome to the gas price notifier bot!\n" \
        "Create a notice about the gas price and the bot will send you a message" \
        " when it is less than the set price.\n" \
        "Use /help for instructions"

help = '/gas_price - get current standard(3 min to confirm) gas price\n' \
       '/fastest, /fast, /standard, /slow - create new notice. Example: "/standard 15"\n' \
       '/get_notices - manage existing notices'

info = 'Data from gasnow.org\n' \
       'Developer @NikitaPirate\n' \
       'Discussion: t.me/gp\\_discussion\n' \
       'Donation:\n' \
       'ETH: `0x0f7387A6E8A8d936aB7F857F523696c0d45a223B`'

gp = '`ETH price:  {} USD\n\n' \
     'Fastest:    {}  (15 sec)\n' \
     'Fast:       {}  (1 min)\n' \
     'Standard:   {}  (3 min)\n' \
     'Slow:       {}  (>10 min)`\n'
