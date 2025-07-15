from models.Runner import Runner
from database import db

class RunnerRepository:

    # GETTERS
    @staticmethod
    def get_all():
        return Runner.query.order_by(Runner.ranking).all()

    @staticmethod
    def get_runner_map():
        return {runner.last_name + "_" + runner.first_name: runner.id for runner in Runner.query.all()}

    @staticmethod
    def get_reward_in_scratch(ranking, sex):
        return Runner.query.filter(Runner.sex_ranking == ranking, Runner.sex == sex).first()
    
    @staticmethod
    def get_reward_in_category(category, sex, skip):
        return Runner.query.filter(Runner.sex == sex, Runner.category == category, Runner.sex_ranking > skip).order_by(Runner.category_ranking).first()

    @staticmethod
    def get_first_oriol(bib, sex):
        return Runner.query.filter(Runner.sex == sex, Runner.oriol == True, ~Runner.bib_number.in_(bib)).order_by(Runner.ranking).first()
    
    #INSERT
    @staticmethod
    def insert_runners(runners):
        db.session.add_all(runners)
        db.session.commit()

    # SETTERS
    @staticmethod
    def update(runner):
        db.session.merge(runner)
        db.session.commit()

    # DELETE
    @staticmethod
    def delete_all():
        Runner.query.delete()
        db.session.commit()
