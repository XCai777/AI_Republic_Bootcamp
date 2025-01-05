// Created by Danielle Bagaforo Meer
// Let's Connect : https://www.linkedin.com/in/algorexph/
import Image from 'next/image';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { ArrowRight, Terminal } from 'lucide-react';

// Add your Projects Here
const projects = [
  {
    title: "Project_1",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_2",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_3",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_4",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_5",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_6",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_7",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_8",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_9",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  {
    title: "Project_10",
    image: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop",
    problem: "Problem",
    solution: "Solution",
    tools: ["Python", "TensorFlow", "Apache Kafka", "MongoDB"],
    link : "https://www.Github.com" // Github Link make sure it has https://
  },
  
];

// Created by Danielle Bagaforo Meer
// Let's Connect : https://www.linkedin.com/in/algorexph/
export default function Projects() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-zinc-900 to-purple-950">

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <h1 className="text-3xl sm:text-4xl font-bold text-white mb-2">ALL PROJECTS</h1>
        <p className="text-gray-400 mb-8 sm:mb-12">Exploring the intersection of AI and real-world solutions</p>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8">
          {projects.map((project, index) => (
            <div key={index} className="group bg-black/40 backdrop-blur-sm border border-purple-500/20 rounded-lg overflow-hidden hover:border-purple-500/40 transition-all duration-300">
              <div className="relative h-48 sm:h-56">
                <Image
                  src={project.image}
                  alt={project.title}
                  fill
                  className="object-cover opacity-60 saturate-50"
                />
                <div className="absolute inset-0 bg-gradient-to-b from-transparent to-black/90" />
              </div>
              
              <div className="p-4 sm:p-6 space-y-4">
                <h3 className="text-lg sm:text-xl font-bold text-purple-400 tracking-tight">{project.title}</h3>
                
                <div className="space-y-4">
                  <div>
                    <h4 className="text-purple-400 text-sm font-semibold uppercase tracking-wider mb-2">PROBLEM:</h4>
                    <p className="text-gray-400 text-sm leading-relaxed">{project.problem}</p>
                  </div>
                  
                  <div>
                    <h4 className="text-purple-400 text-sm font-semibold uppercase tracking-wider mb-2">SOLUTION:</h4>
                    <p className="text-gray-400 text-sm leading-relaxed">{project.solution}</p>
                  </div>
                </div>
                
                <div className="pt-4 space-y-4">
                  <div className="flex flex-wrap gap-2">
                    {project.tools.map((tool, toolIndex) => (
                      <span
                        key={toolIndex}
                        className="text-xs px-3 py-1 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/20"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                  <a href = {project.link} target="_blank" rel="noopener noreferrer">
                  <Button
                    className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium tracking-wide"
                  >
                    VIEW PROJECT
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}

