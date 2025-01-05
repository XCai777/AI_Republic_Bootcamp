// Created by Danielle Bagaforo Meer
// Let's Connect : https://www.linkedin.com/in/algorexph/
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Terminal } from 'lucide-react';

// Add your Skills here
// {name : [Skill] }
const skillCategories = [
  {
    title: "FEATURED",
    skills: [
      { name: "React" },
      { name: "CSS"},
      { name: "HTML" },
      { name: "JavaScript" },
      { name: "Next.js" },
      { name: "SASS" },
      { name: "Flutter" }
    ]
  },
  {
    title: "FRONTEND",
    skills: [
      { name: "React" },
      { name: "CSS"},
      { name: "HTML" },
      { name: "JavaScript" },
      { name: "Next.js" },
      { name: "SASS" },
      { name: "Flutter" }
    ]
  },
  {
    title: "BACKEND",
    skills: [
      { name: "React" },
      { name: "CSS"},
      { name: "HTML" },
      { name: "JavaScript" },
      { name: "Next.js" },
      { name: "SASS" },
      { name: "Flutter" }
    ]
  }
];

const technologies = {
  featured: [
    { name: "React" },
      { name: "CSS"},
      { name: "HTML" },
      { name: "JavaScript" },
      { name: "Next.js" },
      { name: "SASS" },
      { name: "Flutter" }
  ],
  frontend: [
    { name: "React" },
    { name: "CSS"},
    { name: "HTML" },
    { name: "JavaScript" },
    { name: "Next.js" },
    { name: "SASS" },
    { name: "Flutter" }
  ],
  backend: [
    { name: "React" },
      { name: "CSS"},
      { name: "HTML" },
      { name: "JavaScript" },
      { name: "Next.js" },
      { name: "SASS" },
      { name: "Flutter" }
  ]
};

export default function Skills() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    message: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-zinc-900 to-purple-950">
      

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 lg:py-16">
        <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-8 sm:mb-12 lg:mb-16 text-center sm:text-left">SKILLS</h1>

        <div className="space-y-12 sm:space-y-16">
          {skillCategories.map((category, index) => (
            <div key={index} className="space-y-4 sm:space-y-6">
              <h2 className="text-xl sm:text-2xl font-bold text-purple-400 text-center sm:text-left">{category.title}</h2>
              <div className="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-7 gap-3 sm:gap-4">
                {category.skills.map((skill, skillIndex) => (
                  <Badge
                    key={skillIndex}
                    className="py-2 sm:py-3 px-3 sm:px-4 bg-black/40 hover:bg-black/60 border border-purple-500/20 hover:border-purple-500/40 text-white transition-all duration-300 text-sm sm:text-base flex items-center justify-center"
                  >
                    <span className="mr-2 text-base sm:text-lg">{skill.icon}</span>
                    {skill.name}
                  </Badge>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 sm:mt-20 lg:mt-24">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-8 sm:mb-12 lg:mb-16 text-center sm:text-left">
            SOME TECHNOLOGIES I'VE WORKED WITH
          </h2>
          
          <div className="space-y-12 sm:space-y-16">
            {Object.entries(technologies).map(([category, techs]) => (
              <div key={category}>
                <h3 className="text-xl sm:text-2xl font-bold text-purple-400 mb-4 sm:mb-6 text-center sm:text-left">
                  {category.toUpperCase()}
                </h3>
                <div className="grid grid-cols-1 xs:grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3 sm:gap-4">
                  {techs.map((tech, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-center p-3 sm:p-4 bg-black/40 border border-purple-500/20 hover:border-purple-500/40 rounded-lg transition-all duration-300 gap-2"
                    >
                      <span className="text-xl sm:text-2xl">{tech.icon}</span>
                      <span className="text-white font-mono text-sm sm:text-base">{tech.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-16 sm:mt-20 lg:mt-24 mb-8 sm:mb-12">
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4 sm:mb-6 text-center sm:text-left">GET IN TOUCH</h2>
          <p className="text-gray-400 mb-8 sm:mb-12 text-sm sm:text-base text-center sm:text-left">
            Have a project in mind or want to collaborate? I'd love to hear from you. 
            Reach out, and let's create something amazing together!
          </p>

          <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-6 max-w-3xl mx-auto sm:mx-0">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
              <div className="space-y-2">
                <label htmlFor="firstName" className="text-sm text-purple-400">
                  FIRSTNAME*
                </label>
                <Input
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  placeholder="Enter your first name"
                  className="bg-black/40 border-purple-500/20 focus:border-purple-500/40 text-white text-sm sm:text-base"
                  required
                />
              </div>
              <div className="space-y-2">
                <label htmlFor="lastName" className="text-sm text-purple-400">
                  LASTNAME*
                </label>
                <Input
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  placeholder="Enter your last name"
                  className="bg-black/40 border-purple-500/20 focus:border-purple-500/40 text-white text-sm sm:text-base"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="email" className="text-sm text-purple-400">
                EMAIL*
              </label>
              <Input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Enter your email address"
                className="bg-black/40 border-purple-500/20 focus:border-purple-500/40 text-white text-sm sm:text-base"
                required
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="message" className="text-sm text-purple-400">
                MESSAGE*
              </label>
              <Textarea
                id="message"
                name="message"
                value={formData.message}
                onChange={handleChange}
                placeholder="Write your message here"
                className="bg-black/40 border-purple-500/20 focus:border-purple-500/40 text-white min-h-[150px] text-sm sm:text-base"
                required
              />
            </div>

            <Button
              type="submit"
              className="bg-purple-600 hover:bg-purple-700 text-white px-6 sm:px-8 py-2 text-sm sm:text-base w-full sm:w-auto"
            >
              SUBMIT
            </Button>
          </form>
        </div>
      </div>
    </main>
  );
}