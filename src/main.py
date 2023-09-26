import miguel_will_eis as eis
import random
import config

# View at https://www.mentimeter.com/app/presentation/alvvnkz8xctfbt3wqswn8xhoebk8pqo9/vj6jztsvvhqb

if __name__ == "__main__":
    m = eis.mentimeter("al3k17ru81pc")

    while True:
        try:
            random.shuffle(config.words)
            eis_sorte: str = random.choice(config.eis_sorten)
            word: str = "_".join(config.words).format(eis_sorte)

            print(word)
            m.vote(word)
        except KeyboardInterrupt:
            break
