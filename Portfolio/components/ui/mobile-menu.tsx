'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Menu, X } from 'lucide-react';

interface MobileMenuProps {
  links: Array<{
    href: string;
    label: string;
  }>;
}

export function MobileMenu({ links }: MobileMenuProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="sm:hidden">
      <Button
        variant="ghost"
        size="icon"
        className="text-purple-400 hover:text-purple-300 hover:bg-purple-900/20"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? (
          <X className="h-6 w-6" />
        ) : (
          <Menu className="h-6 w-6" />
        )}
      </Button>

      {isOpen && (
        <div className="absolute top-16 left-0 right-0 bg-gradient-to-br from-zinc-900/95 to-purple-950/95 backdrop-blur-md border-b border-purple-500/20 shadow-lg shadow-purple-900/20">
          <div className="flex flex-col space-y-4 px-6 py-8">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="text-purple-300 hover:text-white transition-colors duration-200 text-lg font-medium"
                onClick={() => setIsOpen(false)}
              >
                {link.label}
              </Link>
            ))}
            <Button className="bg-purple-600 hover:bg-purple-700 transition-colors duration-200 mt-2">
              CONTACT
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}