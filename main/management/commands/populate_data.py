from django.core.management.base import BaseCommand
from main.models import (
    DisasterType, EducationModule, Quiz, QuizQuestion, 
    DrillChecklist, DrillStep, EmergencyContact
)

class Command(BaseCommand):
    help = 'Populate database with initial disaster preparedness data'

    def handle(self, *args, **options):
        self.stdout.write('Populating database with initial data...')
        
        # Create disaster types
        earthquake = DisasterType.objects.get_or_create(
            name='Earthquake',
            defaults={
                'description': 'Sudden shaking of the ground caused by movements in the Earth\'s crust',
                'icon': '🌍'
            }
        )[0]
        
        flood = DisasterType.objects.get_or_create(
            name='Flood',
            defaults={
                'description': 'Overflow of water that submerges land that is usually dry',
                'icon': '🌊'
            }
        )[0]
        
        fire = DisasterType.objects.get_or_create(
            name='Fire',
            defaults={
                'description': 'Uncontrolled burning that threatens people and property',
                'icon': '🔥'
            }
        )[0]
        
        # Create education modules
        self.create_earthquake_modules(earthquake)
        self.create_flood_modules(flood)
        self.create_fire_modules(fire)
        
        # Create quizzes
        self.create_earthquake_quiz(earthquake)
        self.create_flood_quiz(flood)
        self.create_fire_quiz(fire)
        
        # Create drill checklists
        self.create_earthquake_drill(earthquake)
        self.create_flood_drill(flood)
        self.create_fire_drill(fire)
        
        # Create emergency contacts
        self.create_emergency_contacts()
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database with initial data'))
    
    def create_earthquake_modules(self, earthquake):
        modules = [
            {
                'title': 'Understanding Earthquakes',
                'content': '''
                <h3>What is an Earthquake?</h3>
                <p>An earthquake is the sudden shaking of the ground caused by movements in the Earth's crust. These movements occur along fault lines where tectonic plates meet.</p>
                
                <h3>Causes of Earthquakes</h3>
                <ul>
                    <li>Movement of tectonic plates</li>
                    <li>Volcanic activity</li>
                    <li>Human activities (mining, dam construction)</li>
                </ul>
                
                <h3>Earthquake Intensity</h3>
                <p>Earthquakes are measured using the Richter scale, ranging from 1-10. Earthquakes above 5.0 can cause significant damage.</p>
                
                <h3>Warning Signs</h3>
                <ul>
                    <li>Small tremors or foreshocks</li>
                    <li>Strange animal behavior</li>
                    <li>Changes in groundwater levels</li>
                </ul>
                ''',
                'order': 1,
                'estimated_read_time': 8
            },
            {
                'title': 'Earthquake Safety During Shaking',
                'content': '''
                <h3>Drop, Cover, and Hold On</h3>
                <p>This is the internationally recommended earthquake safety procedure:</p>
                
                <h4>1. DROP</h4>
                <ul>
                    <li>Drop to your hands and knees immediately</li>
                    <li>Don't try to run to another room</li>
                </ul>
                
                <h4>2. COVER</h4>
                <ul>
                    <li>Take cover under a sturdy desk or table</li>
                    <li>If no table, cover your head and neck with arms</li>
                    <li>Stay away from windows, mirrors, and heavy objects</li>
                </ul>
                
                <h4>3. HOLD ON</h4>
                <ul>
                    <li>Hold onto your shelter and be prepared to move with it</li>
                    <li>Stay in position until shaking stops completely</li>
                </ul>
                
                <h3>If You're Outside</h3>
                <ul>
                    <li>Move away from buildings, trees, and power lines</li>
                    <li>Drop to the ground and protect your head</li>
                </ul>
                ''',
                'order': 2,
                'estimated_read_time': 6
            },
            {
                'title': 'After the Earthquake',
                'content': '''
                <h3>Immediate Actions</h3>
                <ul>
                    <li>Check yourself and others for injuries</li>
                    <li>Provide first aid if needed</li>
                    <li>Check for hazards (gas leaks, electrical damage, structural damage)</li>
                    <li>Turn off utilities if damaged</li>
                </ul>
                
                <h3>Safety Precautions</h3>
                <ul>
                    <li>Be prepared for aftershocks</li>
                    <li>Stay out of damaged buildings</li>
                    <li>Use flashlights, not candles or matches</li>
                    <li>Listen to emergency broadcasts</li>
                </ul>
                
                <h3>Emergency Kit Essentials</h3>
                <ul>
                    <li>Water (1 gallon per person per day for 3 days)</li>
                    <li>Non-perishable food (3-day supply)</li>
                    <li>First aid kit</li>
                    <li>Flashlight and batteries</li>
                    <li>Battery-powered radio</li>
                    <li>Important documents</li>
                </ul>
                ''',
                'order': 3,
                'estimated_read_time': 7
            }
        ]
        
        for module_data in modules:
            EducationModule.objects.get_or_create(
                disaster_type=earthquake,
                order=module_data['order'],
                defaults=module_data
            )
    
    def create_flood_modules(self, flood):
        modules = [
            {
                'title': 'Understanding Floods',
                'content': '''
                <h3>What is a Flood?</h3>
                <p>A flood is an overflow of water that submerges land that is usually dry. Floods can occur suddenly or develop slowly over time.</p>
                
                <h3>Types of Floods</h3>
                <ul>
                    <li><strong>River Floods:</strong> Occur when rivers overflow their banks</li>
                    <li><strong>Flash Floods:</strong> Sudden flooding with little warning</li>
                    <li><strong>Coastal Floods:</strong> Caused by storm surges or tsunamis</li>
                    <li><strong>Urban Floods:</strong> Result from overwhelmed drainage systems</li>
                </ul>
                
                <h3>Causes of Floods</h3>
                <ul>
                    <li>Heavy rainfall</li>
                    <li>Dam or levee failure</li>
                    <li>Rapid snowmelt</li>
                    <li>Storm surges</li>
                    <li>Poor urban drainage</li>
                </ul>
                
                <h3>Warning Signs</h3>
                <ul>
                    <li>Heavy or prolonged rainfall</li>
                    <li>Rising water levels in rivers or streams</li>
                    <li>Water backing up in storm drains</li>
                </ul>
                ''',
                'order': 1,
                'estimated_read_time': 7
            },
            {
                'title': 'Flood Safety and Evacuation',
                'content': '''
                <h3>Before a Flood</h3>
                <ul>
                    <li>Know your area's flood risk</li>
                    <li>Have an evacuation plan</li>
                    <li>Keep emergency supplies ready</li>
                    <li>Stay informed about weather conditions</li>
                </ul>
                
                <h3>During a Flood</h3>
                <ul>
                    <li>Never walk through moving water</li>
                    <li>6 inches of moving water can knock you down</li>
                    <li>Never drive through flooded roads</li>
                    <li>2 feet of rushing water can carry away a vehicle</li>
                    <li>Get to higher ground immediately</li>
                </ul>
                
                <h3>Evacuation Guidelines</h3>
                <ul>
                    <li>Follow official evacuation orders</li>
                    <li>Take emergency supplies with you</li>
                    <li>Turn off utilities before leaving</li>
                    <li>Lock your home and take your keys</li>
                    <li>Follow designated evacuation routes</li>
                </ul>
                
                <h3>Remember: Turn Around, Don't Drown!</h3>
                <p>Most flood-related deaths occur when people attempt to drive through flooded areas.</p>
                ''',
                'order': 2,
                'estimated_read_time': 6
            },
            {
                'title': 'After the Flood',
                'content': '''
                <h3>Returning Home Safely</h3>
                <ul>
                    <li>Wait for authorities to declare it safe</li>
                    <li>Check for structural damage before entering</li>
                    <li>Be aware of contaminated floodwater</li>
                    <li>Document damage with photos</li>
                </ul>
                
                <h3>Health and Safety Precautions</h3>
                <ul>
                    <li>Wear protective clothing when cleaning</li>
                    <li>Discard contaminated food and medicine</li>
                    <li>Clean and disinfect everything that got wet</li>
                    <li>Watch for electrical hazards</li>
                </ul>
                
                <h3>Cleanup Process</h3>
                <ul>
                    <li>Remove standing water</li>
                    <li>Remove wet contents and materials</li>
                    <li>Clean all hard surfaces</li>
                    <li>Dry out the building</li>
                    <li>Contact insurance company</li>
                </ul>
                
                <h3>Preventing Mold Growth</h3>
                <ul>
                    <li>Start cleanup within 24-48 hours</li>
                    <li>Use fans and dehumidifiers</li>
                    <li>Remove wet porous materials</li>
                </ul>
                ''',
                'order': 3,
                'estimated_read_time': 8
            }
        ]
        
        for module_data in modules:
            EducationModule.objects.get_or_create(
                disaster_type=flood,
                order=module_data['order'],
                defaults=module_data
            )
    
    def create_fire_modules(self, fire):
        modules = [
            {
                'title': 'Understanding Fire Hazards',
                'content': '''
                <h3>Types of Fires</h3>
                <ul>
                    <li><strong>Class A:</strong> Ordinary combustibles (wood, paper, fabric)</li>
                    <li><strong>Class B:</strong> Flammable liquids (gasoline, oil, paint)</li>
                    <li><strong>Class C:</strong> Electrical equipment</li>
                    <li><strong>Class D:</strong> Combustible metals</li>
                    <li><strong>Class K:</strong> Cooking oils and fats</li>
                </ul>
                
                <h3>Fire Triangle</h3>
                <p>Fire needs three elements to exist:</p>
                <ul>
                    <li><strong>Heat:</strong> Source of ignition</li>
                    <li><strong>Fuel:</strong> Something to burn</li>
                    <li><strong>Oxygen:</strong> To sustain combustion</li>
                </ul>
                
                <h3>Common Fire Hazards</h3>
                <ul>
                    <li>Faulty electrical wiring</li>
                    <li>Unattended cooking</li>
                    <li>Smoking materials</li>
                    <li>Heating equipment</li>
                    <li>Candles and open flames</li>
                </ul>
                
                <h3>Fire Prevention</h3>
                <ul>
                    <li>Install smoke detectors</li>
                    <li>Keep fire extinguishers accessible</li>
                    <li>Maintain electrical systems</li>
                    <li>Store flammable materials safely</li>
                </ul>
                ''',
                'order': 1,
                'estimated_read_time': 6
            },
            {
                'title': 'Fire Escape Planning',
                'content': '''
                <h3>Creating an Escape Plan</h3>
                <ul>
                    <li>Draw a map of your home/building</li>
                    <li>Identify two exits from each room</li>
                    <li>Choose a meeting place outside</li>
                    <li>Practice the plan regularly</li>
                </ul>
                
                <h3>During a Fire Emergency</h3>
                <ul>
                    <li>Alert others by shouting "FIRE!"</li>
                    <li>Activate fire alarm if available</li>
                    <li>Get out fast - don't gather belongings</li>
                    <li>Test doors before opening them</li>
                    <li>Stay low if there's smoke</li>
                    <li>Close doors behind you</li>
                </ul>
                
                <h3>If Trapped in a Room</h3>
                <ul>
                    <li>Close the door to keep fire out</li>
                    <li>Seal cracks around door with towels</li>
                    <li>Signal for help from window</li>
                    <li>Call emergency services</li>
                </ul>
                
                <h3>Stop, Drop, and Roll</h3>
                <p>If your clothes catch fire:</p>
                <ul>
                    <li><strong>STOP:</strong> Don't run</li>
                    <li><strong>DROP:</strong> Drop to the ground</li>
                    <li><strong>ROLL:</strong> Roll to smother flames</li>
                    <li>Cover your face with hands</li>
                </ul>
                ''',
                'order': 2,
                'estimated_read_time': 7
            },
            {
                'title': 'Fire Safety Equipment',
                'content': '''
                <h3>Smoke Detectors</h3>
                <ul>
                    <li>Install on every level of your home</li>
                    <li>Test monthly</li>
                    <li>Change batteries annually</li>
                    <li>Replace detectors every 10 years</li>
                </ul>
                
                <h3>Fire Extinguishers</h3>
                <ul>
                    <li>Choose the right type for your needs</li>
                    <li>Learn the PASS technique</li>
                    <li>Check pressure gauge regularly</li>
                    <li>Have them professionally inspected</li>
                </ul>
                
                <h3>PASS Technique</h3>
                <ul>
                    <li><strong>P:</strong> Pull the pin</li>
                    <li><strong>A:</strong> Aim at base of fire</li>
                    <li><strong>S:</strong> Squeeze the handle</li>
                    <li><strong>S:</strong> Sweep from side to side</li>
                </ul>
                
                <h3>Fire Blankets</h3>
                <ul>
                    <li>Useful for small fires</li>
                    <li>Can smother flames on clothing</li>
                    <li>Keep in kitchen and workshop areas</li>
                </ul>
                
                <h3>Emergency Ladder</h3>
                <ul>
                    <li>For upper floor escape routes</li>
                    <li>Store near windows</li>
                    <li>Practice using safely</li>
                </ul>
                ''',
                'order': 3,
                'estimated_read_time': 5
            }
        ]
        
        for module_data in modules:
            EducationModule.objects.get_or_create(
                disaster_type=fire,
                order=module_data['order'],
                defaults=module_data
            )
    
    def create_earthquake_quiz(self, earthquake):
        quiz, created = Quiz.objects.get_or_create(
            disaster_type=earthquake,
            title='Earthquake Safety Quiz',
            defaults={'description': 'Test your knowledge of earthquake safety procedures'}
        )
        
        if created:
            questions = [
                {
                    'question_text': 'What is the correct earthquake safety procedure when indoors?',
                    'option_a': 'Run outside immediately',
                    'option_b': 'Stand in a doorway',
                    'option_c': 'Drop, Cover, and Hold On',
                    'option_d': 'Get under a window',
                    'correct_answer': 'C',
                    'explanation': 'Drop, Cover, and Hold On is the internationally recommended procedure for earthquake safety.',
                    'order': 1
                },
                {
                    'question_text': 'How long should you wait after shaking stops before moving?',
                    'option_a': 'Move immediately',
                    'option_b': 'Wait until all shaking completely stops',
                    'option_c': 'Wait 5 minutes',
                    'option_d': 'Wait 1 hour',
                    'correct_answer': 'B',
                    'explanation': 'Wait until all shaking completely stops before moving, as aftershocks may occur.',
                    'order': 2
                },
                {
                    'question_text': 'What should you do if you\'re outside during an earthquake?',
                    'option_a': 'Run into the nearest building',
                    'option_b': 'Move away from buildings, trees, and power lines',
                    'option_c': 'Lie down flat',
                    'option_d': 'Get in a car',
                    'correct_answer': 'B',
                    'explanation': 'Move away from anything that could fall on you, then drop and protect your head.',
                    'order': 3
                },
                {
                    'question_text': 'What magnitude earthquake can cause significant damage?',
                    'option_a': 'Above 2.0',
                    'option_b': 'Above 3.0',
                    'option_c': 'Above 5.0',
                    'option_d': 'Above 8.0',
                    'correct_answer': 'C',
                    'explanation': 'Earthquakes above 5.0 on the Richter scale can cause significant damage.',
                    'order': 4
                },
                {
                    'question_text': 'After an earthquake, what should you check for first?',
                    'option_a': 'Property damage',
                    'option_b': 'Injuries to yourself and others',
                    'option_c': 'Utility damage',
                    'option_d': 'Aftershocks',
                    'correct_answer': 'B',
                    'explanation': 'Always check for injuries first, then assess hazards and damage.',
                    'order': 5
                }
            ]
            
            for q_data in questions:
                QuizQuestion.objects.create(quiz=quiz, **q_data)
    
    def create_flood_quiz(self, flood):
        quiz, created = Quiz.objects.get_or_create(
            disaster_type=flood,
            title='Flood Safety Quiz',
            defaults={'description': 'Test your knowledge of flood safety and preparedness'}
        )
        
        if created:
            questions = [
                {
                    'question_text': 'How much moving water can knock you down?',
                    'option_a': '2 inches',
                    'option_b': '6 inches',
                    'option_c': '1 foot',
                    'option_d': '2 feet',
                    'correct_answer': 'B',
                    'explanation': 'Just 6 inches of moving water can knock you down.',
                    'order': 1
                },
                {
                    'question_text': 'What is the safest action when encountering a flooded road?',
                    'option_a': 'Drive through slowly',
                    'option_b': 'Test the depth first',
                    'option_c': 'Turn around and find another route',
                    'option_d': 'Wait for the water to recede',
                    'correct_answer': 'C',
                    'explanation': 'Turn Around, Don\'t Drown! Never drive through flooded roads.',
                    'order': 2
                },
                {
                    'question_text': 'How much rushing water can carry away a vehicle?',
                    'option_a': '6 inches',
                    'option_b': '1 foot',
                    'option_c': '2 feet',
                    'option_d': '3 feet',
                    'correct_answer': 'C',
                    'explanation': 'Just 2 feet of rushing water can carry away most vehicles.',
                    'order': 3
                },
                {
                    'question_text': 'When should you start flood cleanup to prevent mold?',
                    'option_a': 'Within 1 week',
                    'option_b': 'Within 24-48 hours',
                    'option_c': 'Within 3 days',
                    'option_d': 'Immediately',
                    'correct_answer': 'B',
                    'explanation': 'Start cleanup within 24-48 hours to prevent mold growth.',
                    'order': 4
                },
                {
                    'question_text': 'What type of flood occurs with little warning?',
                    'option_a': 'River flood',
                    'option_b': 'Coastal flood',
                    'option_c': 'Flash flood',
                    'option_d': 'Urban flood',
                    'correct_answer': 'C',
                    'explanation': 'Flash floods occur suddenly with little or no warning.',
                    'order': 5
                }
            ]
            
            for q_data in questions:
                QuizQuestion.objects.create(quiz=quiz, **q_data)
    
    def create_fire_quiz(self, fire):
        quiz, created = Quiz.objects.get_or_create(
            disaster_type=fire,
            title='Fire Safety Quiz',
            defaults={'description': 'Test your knowledge of fire safety and prevention'}
        )
        
        if created:
            questions = [
                {
                    'question_text': 'What are the three elements needed for fire to exist?',
                    'option_a': 'Heat, Fuel, Water',
                    'option_b': 'Heat, Fuel, Oxygen',
                    'option_c': 'Fuel, Oxygen, Carbon',
                    'option_d': 'Heat, Oxygen, Nitrogen',
                    'correct_answer': 'B',
                    'explanation': 'The fire triangle consists of Heat, Fuel, and Oxygen.',
                    'order': 1
                },
                {
                    'question_text': 'What does the "P" in PASS technique stand for?',
                    'option_a': 'Point',
                    'option_b': 'Push',
                    'option_c': 'Pull',
                    'option_d': 'Press',
                    'correct_answer': 'C',
                    'explanation': 'PASS stands for Pull the pin, Aim, Squeeze, Sweep.',
                    'order': 2
                },
                {
                    'question_text': 'If your clothes catch fire, what should you do?',
                    'option_a': 'Run to get help',
                    'option_b': 'Stop, Drop, and Roll',
                    'option_c': 'Pour water on yourself',
                    'option_d': 'Remove the clothes',
                    'correct_answer': 'B',
                    'explanation': 'Stop, Drop, and Roll to smother the flames.',
                    'order': 3
                },
                {
                    'question_text': 'How often should you test smoke detectors?',
                    'option_a': 'Weekly',
                    'option_b': 'Monthly',
                    'option_c': 'Every 3 months',
                    'option_d': 'Annually',
                    'correct_answer': 'B',
                    'explanation': 'Test smoke detectors monthly to ensure they work properly.',
                    'order': 4
                },
                {
                    'question_text': 'What should you do before opening a door during a fire?',
                    'option_a': 'Look through the keyhole',
                    'option_b': 'Listen for sounds',
                    'option_c': 'Test if it\'s hot with the back of your hand',
                    'option_d': 'Open it quickly',
                    'correct_answer': 'C',
                    'explanation': 'Test the door with the back of your hand. If hot, don\'t open it.',
                    'order': 5
                }
            ]
            
            for q_data in questions:
                QuizQuestion.objects.create(quiz=quiz, **q_data)
    
    def create_earthquake_drill(self, earthquake):
        drill, created = DrillChecklist.objects.get_or_create(
            disaster_type=earthquake,
            title='Earthquake Response Drill',
            defaults={'description': 'Practice the Drop, Cover, and Hold On procedure'}
        )
        
        if created:
            steps = [
                {'step_text': 'Feel shaking or hear earthquake warning', 'order': 1, 'is_critical': True, 'time_limit': 5},
                {'step_text': 'Immediately drop to hands and knees', 'order': 2, 'is_critical': True, 'time_limit': 3},
                {'step_text': 'Take cover under sturdy desk or table', 'order': 3, 'is_critical': True, 'time_limit': 5},
                {'step_text': 'If no table available, cover head and neck with arms', 'order': 4, 'is_critical': True, 'time_limit': 3},
                {'step_text': 'Hold onto shelter and be prepared to move with it', 'order': 5, 'is_critical': True, 'time_limit': None},
                {'step_text': 'Stay in position until shaking stops completely', 'order': 6, 'is_critical': True, 'time_limit': None},
                {'step_text': 'After shaking stops, check for injuries', 'order': 7, 'is_critical': False, 'time_limit': 30},
                {'step_text': 'Check for hazards (gas leaks, electrical damage)', 'order': 8, 'is_critical': False, 'time_limit': 60},
                {'step_text': 'Exit building if damaged, watch for aftershocks', 'order': 9, 'is_critical': False, 'time_limit': None},
                {'step_text': 'Go to designated assembly area', 'order': 10, 'is_critical': False, 'time_limit': 120}
            ]
            
            for step_data in steps:
                DrillStep.objects.create(drill_checklist=drill, **step_data)
    
    def create_flood_drill(self, flood):
        drill, created = DrillChecklist.objects.get_or_create(
            disaster_type=flood,
            title='Flood Evacuation Drill',
            defaults={'description': 'Practice flood evacuation procedures'}
        )
        
        if created:
            steps = [
                {'step_text': 'Receive flood warning or observe rising water', 'order': 1, 'is_critical': True, 'time_limit': None},
                {'step_text': 'Alert all occupants', 'order': 2, 'is_critical': True, 'time_limit': 30},
                {'step_text': 'Gather emergency supplies (go-bag)', 'order': 3, 'is_critical': True, 'time_limit': 120},
                {'step_text': 'Turn off utilities (gas, electricity, water)', 'order': 4, 'is_critical': False, 'time_limit': 60},
                {'step_text': 'Secure important documents', 'order': 5, 'is_critical': False, 'time_limit': 30},
                {'step_text': 'Move to higher ground immediately', 'order': 6, 'is_critical': True, 'time_limit': None},
                {'step_text': 'Avoid walking through moving water', 'order': 7, 'is_critical': True, 'time_limit': None},
                {'step_text': 'Do not drive through flooded roads', 'order': 8, 'is_critical': True, 'time_limit': None},
                {'step_text': 'Reach designated evacuation center', 'order': 9, 'is_critical': True, 'time_limit': None},
                {'step_text': 'Check in with authorities and family', 'order': 10, 'is_critical': False, 'time_limit': 60}
            ]
            
            for step_data in steps:
                DrillStep.objects.create(drill_checklist=drill, **step_data)
    
    def create_fire_drill(self, fire):
        drill, created = DrillChecklist.objects.get_or_create(
            disaster_type=fire,
            title='Fire Evacuation Drill',
            defaults={'description': 'Practice fire evacuation procedures'}
        )
        
        if created:
            steps = [
                {'step_text': 'Hear fire alarm or discover fire', 'order': 1, 'is_critical': True, 'time_limit': 5},
                {'step_text': 'Alert others by shouting "FIRE!"', 'order': 2, 'is_critical': True, 'time_limit': 5},
                {'step_text': 'Activate fire alarm if not already activated', 'order': 3, 'is_critical': True, 'time_limit': 10},
                {'step_text': 'Test door before opening (back of hand)', 'order': 4, 'is_critical': True, 'time_limit': 5},
                {'step_text': 'If door is cool, open slowly and check for fire', 'order': 5, 'is_critical': True, 'time_limit': 5},
                {'step_text': 'Use primary exit route', 'order': 6, 'is_critical': True, 'time_limit': 30},
                {'step_text': 'Stay low if there is smoke', 'order': 7, 'is_critical': True, 'time_limit': None},
                {'step_text': 'Close doors behind you as you exit', 'order': 8, 'is_critical': False, 'time_limit': 5},
                {'step_text': 'Go directly to assembly point', 'order': 9, 'is_critical': True, 'time_limit': 60},
                {'step_text': 'Do not re-enter building until cleared by authorities', 'order': 10, 'is_critical': True, 'time_limit': None}
            ]
            
            for step_data in steps:
                DrillStep.objects.create(drill_checklist=drill, **step_data)
    
    def create_emergency_contacts(self):
        contacts = [
            {
                'name': 'National Emergency Services',
                'organization': 'Emergency Response',
                'phone_number': '112',
                'email': '',
                'contact_type': 'medical'
            },
            {
                'name': 'Fire Department',
                'organization': 'Fire and Rescue Services',
                'phone_number': '101',
                'email': '',
                'contact_type': 'fire'
            },
            {
                'name': 'Police Department',
                'organization': 'Local Police',
                'phone_number': '100',
                'email': '',
                'contact_type': 'police'
            },
            {
                'name': 'National Disaster Management Authority',
                'organization': 'NDMA',
                'phone_number': '1078',
                'email': 'ndma@gov.in',
                'contact_type': 'disaster'
            },
            {
                'name': 'State Disaster Management Authority',
                'organization': 'SDMA',
                'phone_number': '1070',
                'email': 'sdma@state.gov.in',
                'contact_type': 'disaster'
            },
            {
                'name': 'Ambulance Service',
                'organization': 'Medical Emergency',
                'phone_number': '108',
                'email': '',
                'contact_type': 'medical'
            }
        ]
        
        for contact_data in contacts:
            EmergencyContact.objects.get_or_create(
                phone_number=contact_data['phone_number'],
                defaults=contact_data
            )
