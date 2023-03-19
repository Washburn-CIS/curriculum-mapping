import inspect
from .curriculumlib import *
from os import listdir

def test_all_topic_references_are_valid():
    for ay in available_years():
        for syllabus in load_syllabi(ay):
            topics = []
            topics.extend(syllabus.topics)
            while topics:
                topic = topics.pop()
                for coverage in topic.coverages:
                    try:
                        standard = load_standard(coverage['standard'])
                        assert isinstance(standard, Standard)
                        topic = standard.topic_coverage_lookup(coverage)
                        assert isinstance(topic, Topic)
                    except:
                        assert False, 'error in ' + ay + ' ' + syllabus.subject + str(syllabus.number) + ' topic ' + str(topic.id)

                topics.extend(topic.subtopics)

def test_all_outcome_references_are_valid():
    for ay in available_years():
        for syllabus in load_syllabi(ay):
            for objective in syllabus.objectives:
                for coverage in objective.coverages:
                    try:
                        standard = load_standard(coverage['standard'])
                        assert isinstance(standard, Standard)
                        outcome = standard.outcome_coverage_lookup(coverage)
                        assert isinstance(outcome, Outcome)
                    except:
                        assert False, 'error in ' + ay + ' ' + syllabus.subject + str(syllabus.number) + ' objective ' + str(objective.id)


########################################################################
# Test Standards
########################################################################

def test_parse_standards():
  standards = load_standards()
  assert len(standards) > 0
  for standard in standards:
    assert isinstance(standard, str)
    assert isinstance(standards[standard], Standard)

def test_cs2017_standard_content():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    assert cs2017
    assert cs2017.name == 'Computer Science Curricula'
    assert cs2017.body == 'acm/ieee'
    assert cs2017.version == '2013'
    assert cs2017.kas
    assert cs2017.kas['SE']
    sp = cs2017.kas['SE']
    assert sp.name == 'Software Engineering'
    assert sp.kas['SVAV']
    svav = sp.kas['SVAV']
    assert svav.name == 'Software Verification and Validation'
    assert len(svav.topics) == 17
    assert len(svav.outcomes) == 17
    topic = svav.topics[1]
    assert topic.text.strip() == 'Inspections, reviews, audits'
    assert topic.importance == 'tier2'
    outcome = svav.outcomes[0]
    assert outcome.text.strip() == 'Distinguish between program validation and verification.'
    assert outcome.importance == 'tier2'
    assert outcome.mastery_level == 'familiarity'

def test_outcome_coverage_list():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    syl = load_syllabus('2019-2020', 'ACT', '324')
    assert syl.get_outcome_coverages()

def test_outcome_coverage_lookup():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    syl = load_syllabus('2019-2020', 'ACT', '324')
    outcome = syl.objectives[0]
    coverage = outcome.coverages[0]
    loutcome = cs2017.outcome_coverage_lookup(coverage)
    assert loutcome

def test_topic_coverage_lookup():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    syl = load_syllabus('2019-2020', 'ACT', '324')
    topic = syl.topics[1]
    subtopic = topic.subtopics[0]
    coverage = subtopic.coverages[0]
    ltopic = cs2017.topic_coverage_lookup(coverage)
    assert ltopic

def test_topic_coverage_lookup_direct():
    standards = load_standards()
    cs2017 = standards['acm-cs2013']
    ka = cs2017.kas['SDF']
    assert ka
    ska = ka.kas['AAD']
    assert ska
    topic = ska.topics[1]
    assert topic
   

def test_every_outcome_coverage():
    standards = load_standards()
    for ay in available_years():
        syllabi = load_syllabi(ay)
        for syllabus in syllabi:
            for outcome in syllabus.objectives:
                for coverage in outcome.coverages:
                    if coverage['standard'] in standards: # todo: change to assertion once all standards are in place
                      standard = standards[coverage['standard']]
                      assert coverage['id'].isdigit(), syllabus.subject + "-" + syllabus.number + " has bad coverage"
                      outcome = standard.outcome_coverage_lookup(coverage)
                      assert outcome is not None, str(coverage) + " outcome not found for" + syllabus.subject + syllabus.number


def test_every_topic_coverage():
    standards = load_standards()
    for ay in available_years():
        syllabi = load_syllabi(ay)
        for syllabus in syllabi:
            topics = syllabus.topics
            while topics:
                topic = topics[0]
                topics = topics[1:]
                if topic.subtopics:
                    topics.extend(topic.subtopics)
                for coverage in topic.coverages:
                    if coverage['standard'] in standards: # todo: change to assertion once all standards are in place
                      standard = standards[coverage['standard']]
                      topic = standard.topic_coverage_lookup(coverage)
                      assert topic is not None, str(coverage) + " topic not found for" + syllabus.subject + syllabus.number


def test_add_coverage():
    standards = load_standards()
    cs2013 = standards['acm-cs2013']
    assert cs2013.outcome_coverage() == 0
    assert cs2013.topic_coverage() == 0
    syl = load_syllabus('2019-2020', 'ACT', '324')
    ka = cs2013.kas['SE']
    assert ka.outcome_coverage() == 0.0
    assert ka.topic_coverage() == 0.0

    # add ACT324 syllabus coverages and check coverage level
    cs2013.add_coverage(syl)
    # TODO: update later with specific number once coverages settle
    assert cs2013.outcome_coverage() > 0
    assert cs2013.topic_coverage() > 0
    assert ka.outcome_coverage() > 0
    assert ka.topic_coverage() > 0 

